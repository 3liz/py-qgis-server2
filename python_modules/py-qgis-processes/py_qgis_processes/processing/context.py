#
#
#
import sys

from pathlib import Path
from string import Template

from typing_extensions import Optional, cast

from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsProcessingContext,
    QgsProject,
)

from py_qgis_contrib.core import logger
from py_qgis_contrib.core.condition import assert_precondition
from py_qgis_contrib.core.config import confservice

from .config import ProcessingConfig
from .utils import get_valid_filename


class ProcessingContext(QgsProcessingContext):

    def __init__(self, config: Optional[ProcessingConfig] = None):
        super().__init__()
        self._destination_project: Optional[QgsProject] = None
        self._config = config or confservice.conf.processing

        self.job_id = "00000000-0000-0000-0000-000000000000"
        self.store_url(f"./jobs/{self._job_id}/files/$resource")
        self.advertised_services_url(f"./ows/{self._job_id}/$name")

    @property
    def job_id(self) -> str:
        return self._job_id

    @job_id.setter
    def job_id(self, ident: str):
        self._job_id = ident
        self._workdir = self._config.workdir.joinpath(ident)
        # Initialize temporaryFolder with workdir
        self.setTemporaryFolder(str(self._workdir))

    def advertised_services_url(self, url: str):
        """ Set advertised_services_url template
        """
        self._advertised_services_url = Template(url)
        if sys.version_info >= (3, 11) and not self._advertised_services_url.is_valid():
            raise ValueError(f"Invalid advertised services url template: {url}")

    def store_url(self, url: str):
        """ Set store_url template
        """
        self._store_url = Template(url)
        if sys.version_info >= (3, 11) and not self._advertised_services_url.is_valid():
            raise ValueError(f"Invalid store url template: {url}")

    @property
    def config(self) -> ProcessingConfig:
        return self._config

    @config.setter
    def config(self, config: ProcessingConfig):
        self._config = config

    @property
    def workdir(self) -> Path:
        return self._workdir

    @property
    def destination_project(self) -> Optional[QgsProject]:
        return self._destination_project

    @destination_project.setter
    def destination_project(self, project: Optional[QgsProject]):
        self._destination_project = project

    def create_project(self, name: str) -> QgsProject:
        """ Create a destination project

            Note: this do NOT set the context destination_project.
        """
        project = self.project()
        if project:
            crs = project.crs()
        else:
            crs = QgsCoordinateReferenceSystem()
            crs.createFromUserInput(self.config.default_crs)
            if not crs.isValid():
                logger.error("Invalid default crs %s", self.config.default_crs)

        destination_project = QgsProject()
        if crs.isValid():
            destination_project.setCrs(crs, self.config.adjust_ellipsoid)

        # Set project filename
        filename = get_valid_filename(name)
        destination_project.setFileName(f"{self.workdir.joinpath(filename)}.qgs")

        # Store files as relative path
        destination_project.setFilePathStorage(Qgis.FilePathType.Relative)

        # Write advertised URLs
        destination_project.writeEntry('WMSUrl', '/', self._ows_reference(name, "WMS"))
        destination_project.writeEntry('WCSUrl', '/', self._ows_reference(name, "WCS"))
        destination_project.writeEntry('WFSUrl', '/', self._ows_reference(name, "WFS"))
        destination_project.writeEntry('WMTSUrl', '/', self._ows_reference(name, "WMTS"))

        return destination_project

    def store_reference_url(self, resource: str) -> str:
        """ Return a proper reference url for the resource
        """
        return self._store_url.substitute(resource=resource)

    def file_reference(self, path: Path) -> str:
        return self.store_reference_url(str(path.relative_to(self.workdir)))

    def _ows_reference(
        self,
        name: str,
        service: Optional[str],
        request: Optional[str] = None,
        query: Optional[str] = None,
    ) -> str:
        service = service or "WMS"
        request = request or "GetCapabilities"
        url = (
            f"{self._advertised_services_url.substitute(name=name)}"
            f"?SERVICE={service}&REQUEST={request}"
        )
        if query:
            url = f"{url}&{query}"

        return url

    def ows_reference(
        self,
        *,
        service: Optional[str],
        request: Optional[str] = None,
        query: Optional[str] = None,
    ) -> str:
        assert_precondition(self._destination_project is not None, "Destination project required")
        return self._ows_reference(
            Path(cast(QgsProject, self._destination_project).fileName()).stem,
            service,
            request,
            query,
        )