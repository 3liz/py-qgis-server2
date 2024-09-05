
import inspect
import types

from functools import cached_property

import celery
import celery.states

from pydantic import (
    BaseModel,
    JsonValue,
    TypeAdapter,
    ValidationError,
    create_model,
)
from typing_extensions import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterator,
    Optional,
    Tuple,
    Type,
    TypeAlias,
)

# from as_core.storage import StorageClient, StorageCreds, storage_client
from py_qgis_contrib.core import logger
from py_qgis_contrib.core.utils import to_iso8601, utc_now

from ._celery import Celery, CeleryConfig

#
#  Worker
#

JobContext: TypeAlias = types.SimpleNamespace


class Worker(Celery):

    def __init__(self, name: str, conf: CeleryConfig, **kwargs):

        super().__init__(name, conf, **kwargs)

        # See https://docs.celeryq.dev/en/stable/userguide/routing.html
        # for task routing

        self._name = name
        self._job_context: Dict[str, Any] = {}

        # See https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-worker_prefetch_multiplier
        self.conf.worker_prefetch_multiplier = 1

        # Logging
        self.conf.worker_redirect_stdouts = False
        self.conf.worker_hijack_root_logger = False

        self._autoscale = conf.autoscale

    @cached_property
    def worker_hostname(self) -> str:
        import socket
        return f"{self._name}@{socket.gethostname()}"

    def start_worker(self, **kwargs) -> None:
        """ Start the worker
        """
        if self._autoscale:
            # Activate autoscale
            kwargs.update(autoscale=(max(self.autoscale), min(self.autoscale)))

        worker = self.Worker(
            hostname=self.worker_hostname,
            prefetch_multiplier=1,
            optimization='fair',
            **kwargs,
        )

        worker.start()

    def job(
        self,
        name: str,
        *args,
        **kwargs,
    ) -> celery.Task:
        """ Decorator for creating job tasks

            Extra options:

            'run_context: bool'
                If set to true
                the context metadata objet will be passed as the first
                positional argument.  The argument should be treated
                as a positional argument only (https://peps.python.org/pep-0570/)
                in order to not beeing included in the run config model.

            Exemple:
                @app.job(name='echo', bind=True, run_context=True)
                def main(self, ctx, /, *args, **kwargs):
                    return f"got customer id : {ctx.customer_id}"
        """
        base = kwargs.pop('base', Job)
        return super().task(
            *args,
            name=f"{self.main}.{name}",
            base=base,
            track_started=True,
            _worker_job_context=self._job_context,
            **kwargs,
        )


# Create a dict class on wich we can
# add attributes
class _Dict(dict):
    pass


#
# Celery task override
#

class Job(celery.Task):

    _worker_job_context: ClassVar[Dict] = {}

    # To be set in decorator
    run_context: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Analyse argument and build the
        # run config schema

        self.typing = False  # Disable argument type checking
        self.__config__ = create_job_run_config(self.__wrapped__)

    def __call__(self, *args, **kwargs):
        #
        # Override the call method in order to validate
        # the json input
        #
        _, outputs = self.__config__

        meta = kwargs.pop('__meta__')  # Remove metadata from arguments

        if self.run_context:
            args = (meta.__context__,)
        else:
            args = ()

        out = self.run(*args, **meta.__run_config__.__dict__)
        # Return output as json compatible format
        return outputs.dump_python(out, mode='json', by_alias=True, exclude_none=True)

    def before_start(self, task_id, args, kwargs):
        #
        # We expect the following as arguments:
        #
        #  A '__context__' dictionary that hold metadata informations
        #  for tasks. This will be passed as JobContext to the task.
        #
        #  A '__meta__' entry that will
        #  add update infos stored in the backend into the 'kwargs' key.
        #
        #  A '__run_config__' dictionary holding task arguments
        #
        # Encode metadata into kwargs; they will be
        # stored in the backend
        # This is a workaround for adding extra metadata
        # with the stored backend data.

        context = kwargs.pop('__context__', {})
        context.update(self._worker_job_context)
        context.update(task_id=task_id)

        meta = kwargs.pop('__meta__', {})
        meta.update(
            started=utc_now(),
        )

        meta = _Dict(meta)

        run_config = kwargs.pop('__run_config__', kwargs)
        # Validate arguments
        #
        # We do not validate arguments in __call__ because
        # we want the error being stored as json object
        # in the __meta__ (see above) and not as a textual
        # dump of the raised exception in the 'result' field.
        try:
            # Store as meta attributes so that they wont be visible
            # as kwargs in backend data
            inputs, _ = self.__config__
            meta.__run_config__ = inputs.model_validate(run_config)
            logger.debug("%s: run config: %s", task_id, meta.__run_config__)
            meta.__context__ = JobContext(**context)
            # Replace kw arguments by the run configuration
            if kwargs is not run_config:
                kwargs.clear()
                kwargs.update(run_config)
        except ValidationError as e:
            errors = [d for d in e.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            )]
            meta.update(errors=errors)
            logger.error("Invalid arguments for %s: %s:", task_id, errors)
            raise ValueError("Invalid arguments")
        finally:
            kwargs.update(__meta__=meta)

    def set_progress(
        self,
        percent_done: Optional[float] = None,
        message: Optional[str] = None,
    ):
        """ Update progress info
            percent: the process percent betwee 0. and 1.
        """
        self.update_state(
            state=Worker.STATE_UPDATED,
            meta=dict(
                progress=int(percent_done + 0.5) if percent_done is not None else None,
                message=message,
                updated=to_iso8601(utc_now()),
            ),
        )


#
# Run configs
#

class RunConfig(BaseModel, frozen=True, extra='ignore'):
    """Base config model for tasks
    """
    pass


def create_job_run_config(wrapped: Callable) -> Tuple[Type[RunConfig], TypeAdapter]:
    """ Build a RunConfig from fonction signature
    """
    s = inspect.signature(wrapped)
    qualname = wrapped.__qualname__

    def _models() -> Iterator[Tuple[str, Any]]:
        for p in s.parameters.values():
            match p.kind:
                case p.POSITIONAL_ONLY | p.VAR_POSITIONAL | p.VAR_KEYWORD:
                    continue
                case p.POSITIONAL_OR_KEYWORD | p.KEYWORD_ONLY:
                    if p.annotation is inspect.Signature.empty:
                        raise TypeError(
                            "Missing annotation for argument "
                            f"{p.name} in job {qualname}",
                        )
                    has_default = p.default is not inspect.Signature.empty
                    yield p.name, (
                        p.annotation,
                        p.default if has_default else ...,
                    )

    _inputs = {name: model for name, model in _models()}

    # Inputs
    inputs = create_model(
        "_RunConfig",
        __base__=RunConfig,
        **_inputs,
    )

    # Outputs
    if s.return_annotation is not inspect.Signature.empty:
        return_annotation = s.return_annotation
    else:
        return_annotation = None

    outputs: TypeAdapter = TypeAdapter(return_annotation or JsonValue)

    return (inputs, outputs)