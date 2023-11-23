from pydantic import AfterValidator, AnyHttpUrl, Field, Json
from typing_extensions import Annotated, List, Optional

from py_qgis_cache.config import ProjectsConfig
from py_qgis_contrib.core import config, logger
from py_qgis_contrib.core.config import NetInterface, SSLConfig, section
from py_qgis_contrib.core.qgis import QgisPluginConfig

DEFAULT_INTERFACE = ("[::]", 23456)

#
# Service SSL configuration
#


def _check_ssl_config(sslconf):
    match (sslconf.key, sslconf.cert):
        case (str(), None):
            raise ValueError("Missing ssl cert file")
        case (None, str()):
            raise ValueError("Missinc ssl key file")
    return sslconf


class ListenConfig(config.Config):
    listen: NetInterface = Field(
        default=DEFAULT_INTERFACE,
        title="TCP:PORT interface or unix socket",
    )
    ssl: Annotated[
        SSLConfig,
        AfterValidator(_check_ssl_config)
    ] = SSLConfig()


class WorkerConfig(config.Config):
    name: str = Field(
        default="default",
        title="Name of the worker instance",
    )
    description: str = Field(
        default="",
        title="Description",
        description="Description for administrative purpose",
    )
    projects: ProjectsConfig = Field(
        default=ProjectsConfig(),
        title="Projects configuration",
        description="Projects and cache configuration",
    )
    max_projects: int = Field(
        default=50,
        title="Max number of projects in cache",
        description=(
            "The maximum number of projects allowed in cache. "
            "The default value is set to 50 projects. "
        )
    )
    load_project_on_request: bool = Field(
        default=True,
        title="Load project in cache when requested",
        description=(
            "Load project in cache at request. "
            "If set to 'false', project not loaded in cache will "
            "return a 403 HTTP code when requested. "
            "Thus, adding project's to cache will require a specific "
            "action from another service or admininstrative "
            "management tools."
        )
    )
    reload_outdated_project_on_request: bool = Field(
        default=False,
        title="Reload outdated project when requested",
        description=(
            "Reload outdated project at request. "
            "If set to 'false', outdated project in cache will "
            "not be refreshed when requested. "
            "Thus, refreshing project's to cache will require a specific "
            "action from another service or admininstrative "
            "management tools."
        )
    )
    plugins: QgisPluginConfig = Field(
        default=QgisPluginConfig(),
        title="Plugins configuration",
    )
    max_chunk_size: int = Field(
        default=1024 * 1024,
        title="Maximum chunk size",
        description="Set the maximum chunk size for streamed responses.",
    )
    interfaces: List[ListenConfig] = Field(
        default=[ListenConfig()],
        title="Interfaces to listen to",
        min_length=1,
    )
    max_waiting_requests: int = Field(
        default=20,
        title="Max number of concurrent requests",
        description=(
            "The maximum number of requests that can be "
            "queued for this worker task. If the number of "
            "waiting requests reach the limit, the subsequent "
            "requests will be returned with a `service unavailable` "
            "error"
        ),
    )
    worker_timeout: int = Field(
        default=20,
        title="Stalled worker timeout",
        description=(
            "Set the amount of time in seconds before considering "
            "considering that the worker is stalled. "
            "A stalled worker will be terminated and the server will "
            "exit with an error code"
        ),
    )
    shutdown_grace_period: int = Field(
        default=20,
        title="Shutdown grace period",
        description=(
            "The maximum amount of time to wait before "
            "closing connections. During this period, "
            "no new connections are allowed."
        ),
    )
    max_worker_failure_pressure: float = Field(
        default=0.,
        title="Max worker failure pressure",
        description=(
            "The maximum ratio of terminated/initial workers "
            "allowed. If this limit is reached,  the server will "
            "issue a critical failure before exiting."
        ),
    )


EXTERNAL_CONFIG_SECTION = "config_url"


class RemoteConfigError(Exception):
    pass


@section(EXTERNAL_CONFIG_SECTION)
class ConfigUrl(config.Config):
    """
    Url for external configuration.
    The configuration is fetched from the remote url
    at startup and override all local settings.
    """
    ssl: Optional[SSLConfig] = None
    url: Optional[AnyHttpUrl] = Field(
        default=None,
        title="External configuration Url",
        description=(
            "Url to external configuration. "
            "The server will issue a GET method against this url at startup. "
            "The method should returns a valid configuration fragment. "
        ),
    )

    def is_set(self) -> bool:
        return self.url is not None

    async def load_configuration(self) -> Optional[Json]:
        """ Load remote configuration and return the Json
            object
        """
        if not self.url:
            return None

        import aiohttp

        if self.url.scheme == 'https':
            import ssl
            if self.ssl:
                ssl_context = ssl.create_default_context(cafile=self.ssl.ca)
                if self.ssl.cert:
                    ssl_context.load_cert_chain(self.ssl.cert, self.ssl.key)
            else:
                ssl_context = ssl.create_default_context()
        else:
            ssl_context = False

        async with aiohttp.ClientSession() as session:
            logger.info("** Loading configuration from %s **", self.url)
            try:
                async with session.get(str(self.url), ssl=False) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        raise RemoteConfigError(
                            f"Failed to get configuration from {self.url} (error {resp.status})",
                        )
            except aiohttp.ClientConnectorSSLError as err:
                raise RemoteConfigError(str(err))


#
# Environment variables
#
ENV_CONFIGFILE = "PY_QGIS_WORKER_CONFIGFILE"
ENV_NUM_PROCESSES = "PY_QGIS_WORKER_NUM_PROCESSES"
