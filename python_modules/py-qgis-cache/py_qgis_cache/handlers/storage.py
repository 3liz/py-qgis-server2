#
# Copyright 2023 3liz
# Author David Marteau
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" Generic protocol handler for Qgis storage
"""
import traceback

from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Iterator, Optional, Type, TypeAlias
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from qgis.core import Qgis, QgsApplication, QgsProject, QgsProjectStorage

from py_qgis_contrib.core import componentmanager, logger

from ..common import IProtocolHandler, ProjectMetadata, Url
from ..config import ProjectsConfig
from ..storage import load_project_from_uri

__all__ = []  # type: ignore


ResolverFactory: TypeAlias = Type['_UrlResolver'] | Callable[[], '_UrlResolver']

RESOLVERS: Dict[str, ResolverFactory] = {}


def resolver_for(name: str) -> Callable:
    """ Decorator for resolver
    """
    def wrapper(klass: Type[_UrlResolver]) -> Type[_UrlResolver]:
        RESOLVERS[name] = klass
        return klass
    return wrapper


#
# Default storage uri resolvers
#
# A resolver normalize an input url
# so that it can be used by the
# corresponding project's storage
#
# Usually, it takes the path
# of the url as the project's name
# and set it to the appropriate
# query argument
#
# This is unfortunate that Qgis
# does not have some canonical
# form for storage uri
#
class _UrlResolver:
    parameter: str = "project"

    def resolve_url(self, url: Url) -> str:
        qs = parse_qs(url.query)
        # Check that the parameter is not already
        # defined in the query string
        if self.parameter not in qs:
            qs[self.parameter] = [url.path]
            url = url._replace(path="", query=urlencode(qs, doseq=True))
        return urlunsplit(url)

    def build_path(self, url: str | Url, location: str, _: Url) -> str:
        if isinstance(url, str):
            url = urlsplit(url)
        return str(Path(location).joinpath(
            parse_qs(url.query)[self.parameter][0],
        ))


@resolver_for('postgresql')
class PosgresqlResolver(_UrlResolver):
    # Postgres storage use 'project' as parameter
    pass


@resolver_for('geopackage')
class GeopackageResolver(_UrlResolver):
    parameter = 'projectName'


#
# Handlers registration
#


def register_handlers(resolvers: Optional[Dict[str, ResolverFactory]] = None):
    """ Register storage handlers as protocol handlers
    """
    resolvers = resolvers or RESOLVERS
    sr = QgsApplication.projectStorageRegistry()
    for ps in sr.projectStorages():
        storage = ps.type()
        logger.info("### Registering storage handler for %s", storage)
        resolver = resolvers.get(storage) or _UrlResolver
        componentmanager.gComponentManager.register_service(
            f'@3liz.org/cache/protocol-handler;1?scheme={storage}',
            QgisStorageProtocolHandler(ps, resolver()),
        )


def load_resolvers(confdir: Path):
    """ Load resolvers configuration
    """
    # XXX Require that resolver file mode is not writable
    # by 'other'
    resolver_file = confdir.joinpath('resolvers.py')
    if resolver_file.exists():
        logger.info("Loading path resolvers for qgis storage")
        with resolver_file.open() as source:
            try:
                exec(source.read(), {
                    'resolver_for': resolver_for,
                    'qgis_version': Qgis.QGIS_VERSION_INT,
                })
            except Exception:
                traceback.print_exc()
                raise RuntimeError(f"Failed to load resolver '{resolver_file}'") from None
    else:
        logger.info("No storage path resolvers found")


def init_storage_handlers(confdir: Optional[Path]):
    """ Initialize storage handlers from resolver file
    """
    if confdir:
        load_resolvers(confdir)
    register_handlers()

#
# Storage protocol handler implementation
#


class QgisStorageProtocolHandler(IProtocolHandler):
    """ Handle postgres protocol
    """
    def __init__(
            self,
            storage: QgsProjectStorage,
            resolver: Optional[_UrlResolver] = None,
    ):
        self._storage = storage
        self._resolver = resolver

    def resolve_uri(self, url: Url) -> str:
        """ Override
        """
        return self._resolver.resolve_url(url) if self._resolver else urlunsplit(url)

    def public_path(self, url: str | Url, location: str, rooturl: Url) -> str:
        """ Override
        """
        if self._resolver:
            return self._resolver.build_path(url, location, rooturl)
        else:
            if isinstance(url, str):
                url = urlsplit(url)
            return str(Path(location).joinpath(url.path))

    def project_metadata(self, url: Url | ProjectMetadata) -> ProjectMetadata:
        """ Override
        """
        if isinstance(url, ProjectMetadata):
            uri = url.uri
        else:
            uri = self.resolve_uri(url)

        # Precondition
        # If there is problem here, then it comes from the
        # path resolver configuration
        assert self._storage.isSupportedUri(uri), f"Invalide uri for storage '{self._storage.type()}': {uri}"
        return self._project_storage_metadata(uri, url.scheme)

    def project(self, md: ProjectMetadata, config: ProjectsConfig) -> QgsProject:
        """ Override
        """
        return load_project_from_uri(md.uri, config)

    def projects(self, url: Url) -> Iterator[ProjectMetadata]:
        """ Override
        """
        uri = urlunsplit(url)
        # Precondition
        # If there is problem here, then it comes from the
        # path resolver configuration
        assert self._storage.isSupportedUri(uri), f"Unsupported {uri} for '{self._storage.type()}'"

        for _uri in self._storage.listProjects(uri):
            yield self._project_storage_metadata(_uri, url.scheme)

    def _project_storage_metadata(self, uri: str, scheme: str) -> ProjectMetadata:
        """ Read metadata about project
        """
        res, md = self._storage.readProjectStorageMetadata(uri)
        if not res:
            logger.error("Failed to read storage metadata for %s", uri)
            raise FileNotFoundError(uri)
        # XXX
        last_modified = md.lastModified.toPyDateTime()
        return ProjectMetadata(
            uri=uri,
            name=md.name,
            scheme=scheme,
            storage=self._storage.type(),
            last_modified=int(datetime.timestamp(last_modified)),
        )
