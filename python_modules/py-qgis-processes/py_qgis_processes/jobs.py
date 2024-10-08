#
# Processing jobs
#


from celery.signals import worker_process_init
from typing_extensions import (
    Optional,
)

from py_qgis_contrib.core.celery import Job, JobContext

from .schemas import (
    JobExecute,
    JobResults,
)
from .worker.prelude import (
    Feedback,
    ProcessCacheProto,
    QgisJob,
    QgisProcessJob,
    QgisWorker,
)
from .worker.processing import (
    ProcessingCache,
    QgisProcessingContext,
)

#
#  Signals
#

# Called at process initialization
# See https://docs.celeryq.dev/en/stable/userguide/signals.html#worker-process-init


@worker_process_init.connect
def init_qgis(*args, **kwargs):
    """ Initialize Qgis context in each process
    """
    QgisProcessingContext.setup_processing(app.processing_config)

#
# Qgis Worker
#


class QgisProcessingWorker(QgisWorker):

    def create_context(self) -> QgisProcessingContext:
        return QgisProcessingContext(self.processing_config, service_name=self.service_name)

    def create_processes_cache(self) -> Optional[ProcessCacheProto]:
        processes_cache = ProcessingCache(self.processing_config)
        processes_cache.start()
        return processes_cache


app = QgisProcessingWorker()

#
# Processing tasks
#


@app.job(name="process_validate", base=QgisJob)
def validate_process_inputs(
    self: Job,
    ctx: JobContext,
    /,
    ident: str,
    request: JobExecute,
    project_path: Optional[str] = None,
):
    """Validate process inputs without executing
    """
    ctx.qgis_context.validate(
        ident,
        request,
        feedback=Feedback(self.setprogress),
        project_path=project_path,
    )


@app.job(name="process_execute", bind=True, run_context=True, base=QgisProcessJob)
def execute_process(
    self: Job,
    ctx: JobContext,
    /,
    ident: str,
    request: JobExecute,
    project_path: Optional[str] = None,
) -> JobResults:
    """Execute process
    """
    # Optional context attributes
    public_url: str | None
    try:
        public_url = ctx.public_url
    except AttributeError:
        public_url = None

    result, _ = ctx.qgis_context.execute(
        ctx.task_id,
        ident,
        request,
        feedback=Feedback(self.set_progress),
        project_path=project_path,
        public_url=public_url,
    )

    # Move files to store
    self.app.store_files(ctx.task_id)

    return result
