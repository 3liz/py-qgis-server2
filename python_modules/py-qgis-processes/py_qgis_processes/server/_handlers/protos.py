from aiohttp import web
from pydantic import TypeAdapter
from typing_extensions import Optional, Protocol

from ...executor import (
    Executor,
    InputValueError,
    JobExecute,
    JobResults,
    JobStatus,
    JsonDict,
    PresenceDetails,
    ProcessDescription,
    ProcessSummary,
)
from .. import swagger
from ..accesspolicy import AccessPolicy
from ..cache import ProcessesCache
from ..jobrealm import JOB_REALM_HEADER, get_job_realm, job_realm
from ..models import ErrorResponse
from ..utils import Link, href, make_link, public_url

swagger.model(JobExecute)
swagger.model(JobStatus)


JobResultsAdapter = TypeAdapter(JobResults)

swagger.model(JobResultsAdapter, "JobResults")


class HandlerProto(Protocol):
    _executor: Executor
    _accesspolicy: AccessPolicy
    _timeout: int
    _cache: ProcessesCache

    def get_service(self, request: web.Request, raise_error: bool = True) -> str:
        ...

    def get_project(self, request: web.Request) -> Optional[str]:
        ...

    def format_path(
        self,
        request: web.Request,
        path: str,
        service: Optional[str] = None,
        project: Optional[str] = None,
        *,
        query: Optional[str] = None,
    ) -> str:
        ...