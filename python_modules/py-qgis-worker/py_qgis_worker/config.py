from py_qgis_contrib.core import config
from py_qgis_contrib.core.qgis import QgisPluginConfig
from py_qgis_project_cache.config import ProjectsConfig

from pydantic import (
    Field,
)
from typing_extensions import (
    List,
    Optional,
)

DEFAULT_INTERFACE = ("0.0.0.0", 23456)


class WorkerConfig(config.Config):
    name: str = Field(
        title="Name of the worker configuration",
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
        default=True,
        title="Reload outdated project when requested",
        description=(
            "Reload outdated project at request. "
            "If set to 'false', outdated project in cache will "
            "not be refrested when requested. "
            "Thus, refreshing project's to cache will require a specific "
            "action from another service or admininstrative "
            "management tools."
        )
    )
    plugins: QgisPluginConfig = Field(
        default=QgisPluginConfig(),
        title="Plugins configuration",
    )
    interfaces: config.NetInterface = Field(
        default=[DEFAULT_INTERFACE],
        title="Interfaces to listen to",
    )
    ssl: Optional[config.SSLConfig] = Field(
        default=None,
        title="SSL/TLS configuration",
    )


@config.section("workspace")
class WorkespaceConfig(config.Config):
    workers: List[WorkerConfig] = Field(
        default=[WorkerConfig(name='default')],
        title="List of worker configuration",
        description=(
            "Configurations for workers. "
            "Each workers can be configured with a "
            "specific configuration."
        )
    )

    def get_worker_config(self, name: str):
        for w in self.workers:
            if w.name == name:
                return w
        raise KeyError(name)
