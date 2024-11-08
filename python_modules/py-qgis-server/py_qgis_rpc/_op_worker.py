""" Implement Qgis server worker
    as a sub process
"""
import os
import signal
import traceback

from multiprocessing.connection import Connection

# See https://stackoverflow.com/questions/75630114/multiprocessing-and-event-type-hint-issue-python
from multiprocessing.synchronize import Event as EventClass
from time import sleep, time

import psutil

from pydantic import JsonValue
from typing_extensions import Optional, assert_never, cast

from qgis.core import QgsFeedback
from qgis.server import QgsServer

from py_qgis_cache import CacheManager, CheckoutStatus, ProjectMetadata
from py_qgis_contrib.core import logger
from py_qgis_contrib.core.config import ConfigProxy
from py_qgis_contrib.core.qgis import (
    PluginType,
    QgisPluginService,
    init_qgis_server,
    show_all_versions,
    show_qgis_settings,
)

from . import _op_cache, _op_plugins, _op_requests
from . import messages as _m
from .config import WorkerConfig
from .delegate import ApiDelegate

Co = CheckoutStatus


def load_default_project(cm: CacheManager):
    """ Load default project
    """
    default_project = os.getenv("QGIS_PROJECT_FILE")
    if default_project:
        url = cm.resolve_path(default_project, allow_direct=True)
        md, status = cm.checkout(url)
        if status == Co.NEW:
            cm.update(cast(ProjectMetadata, md), status)
        else:
            logger.error("The project %s does not exists", url)


def setup_server(conf: WorkerConfig) -> QgsServer:
    """ Setup Qgis server and plugins
    """
    # Enable qgis server debug verbosity
    if logger.is_enabled_for(logger.LogLevel.DEBUG):
        os.environ['QGIS_SERVER_LOG_LEVEL'] = '0'
        os.environ['QGIS_DEBUG'] = '1'

    projects = conf.projects
    if projects.trust_layer_metadata:
        os.environ['QGIS_SERVER_TRUST_LAYER_METADATA'] = 'yes'
    if projects.disable_getprint:
        os.environ['QGIS_SERVER_DISABLE_GETPRINT'] = 'yes'

    # Disable any cache strategy
    os.environ['QGIS_SERVER_PROJECT_CACHE_STRATEGY'] = 'off'

    server = init_qgis_server(settings=conf.qgis_settings)

    CacheManager.initialize_handlers(projects)

    if logger.is_enabled_for(logger.LogLevel.DEBUG):
        print(show_qgis_settings())  # noqa T201

    return server


def worker_env() -> JsonValue:
    from qgis.core import Qgis
    return dict(
        qgis_version=Qgis.QGIS_VERSION_INT,
        qgis_release=Qgis.QGIS_RELEASE_NAME,
        versions=list(show_all_versions()),
        environment=dict(os.environ),
    )


class Feedback:
    def __init__(self) -> None:
        self._feedback: Optional[QgsFeedback] = None

        def _cancel(*args) -> None:
            if self._feedback:
                self._feedback.cancel()

        signal.signal(signal.SIGHUP, _cancel)

    def reset(self) -> None:
        self._feedback = None

    @property
    def feedback(self) -> QgsFeedback:
        if not self._feedback:
            self._feedback = QgsFeedback()
        return self._feedback

#
# Run Qgis server
#


def qgis_server_run(
    server: QgsServer,
    conn: Connection,
    conf: WorkerConfig,
    event: EventClass,
    name: str = "",
    reporting: bool = True,
):
    """ Run Qgis server and process incoming requests
    """
    cm = CacheManager(conf.projects, server)

    # Register the cache manager as a service
    cm.register_as_service()

    server_iface = server.serverInterface()

    # Load plugins
    plugin_s = QgisPluginService(conf.plugins)
    plugin_s.load_plugins(PluginType.SERVER, server_iface)

    # Register as a service
    plugin_s.register_as_service()

    # Register delegation api
    api_delegate = ApiDelegate(server_iface)
    server_iface.serviceRegistry().registerApi(api_delegate)

    load_default_project(cm)

    # For reporting
    _process = psutil.Process() if reporting else None

    feedback = Feedback()

    event.set()
    while True:
        logger.trace("%s: Waiting for messages", name)
        try:
            msg = conn.recv()
            event.clear()
            logger.debug("Received message: %s", msg.msg_id.name)
            logger.trace(">>> %s: %s", msg.msg_id.name, msg.__dict__)
            _t_start = time()
            match msg.msg_id:
                # --------------------
                # Qgis server Requests
                # --------------------
                case _m.MsgType.OWSREQUEST:
                    _op_requests.handle_ows_request(
                        conn,
                        msg,
                        server,
                        cm,
                        conf,
                        _process,
                        cache_id=name,
                        feedback=feedback.feedback,
                    )
                case _m.MsgType.APIREQUEST:
                    _op_requests.handle_api_request(
                        conn,
                        msg,
                        server,
                        cm,
                        conf,
                        _process,
                        cache_id=name,
                        feedback=feedback.feedback,
                    )
                case _m.MsgType.REQUEST:
                    _op_requests.handle_generic_request(
                        conn,
                        msg,
                        server,
                        cm,
                        conf,
                        _process,
                        cache_id=name,
                        feedback=feedback.feedback,
                    )
                # --------------------
                # Global management
                # --------------------
                case _m.MsgType.PING:
                    _m.send_reply(conn, msg.echo)
                case _m.MsgType.QUIT:
                    _m.send_reply(conn, None)
                    break
                # --------------------
                # Cache management
                # --------------------
                case _m.MsgType.CHECKOUT_PROJECT:
                    _op_cache.checkout_project(conn, cm, conf, msg.uri, msg.pull, cache_id=name)
                case _m.MsgType.DROP_PROJECT:
                    _op_cache.drop_project(conn, cm, msg.uri, name)
                case _m.MsgType.CLEAR_CACHE:
                    cm.clear()
                    _m.send_reply(conn, None)
                case _m.MsgType.LIST_CACHE:
                    _op_cache.send_cache_list(conn, cm, msg.status_filter, cache_id=name)
                case _m.MsgType.UPDATE_CACHE:
                    _op_cache.update_cache(conn, cm, cache_id=name)
                case _m.MsgType.PROJECT_INFO:
                    _op_cache.send_project_info(conn, cm, msg.uri, cache_id=name)
                case _m.MsgType.CATALOG:
                    _op_cache.send_catalog(conn, cm, msg.location)
                # --------------------
                # Plugin inspection
                # --------------------
                case _m.MsgType.PLUGINS:
                    _op_plugins.inspect_plugins(conn, plugin_s)
                # --------------------
                # Config
                # --------------------
                case _m.MsgType.PUT_CONFIG:
                    if isinstance(conf, ConfigProxy):
                        confservice = conf.service
                        confservice.update_config(msg.config)
                        # Update log level
                        logger.set_log_level(confservice.conf.logging.level)
                        _m.send_reply(conn, None)
                    else:
                        # It does no make sense to update configuration
                        # If the configuration is not a proxy
                        # since cache manager and others will hold immutable
                        # instance of configuration
                        _m.send_reply(conn, "", 403)
                case _m.MsgType.GET_CONFIG:
                    _m.send_reply(conn, conf.model_dump())
                # --------------------
                # Status
                # --------------------
                case _m.MsgType.ENV:
                    _m.send_reply(conn, worker_env())
                # --------------------
                # Test
                # --------------------
                case _m.MsgType.TEST:
                    run_test(conn, msg, feedback.feedback)
                # --------------------
                case _ as unreachable:
                    assert_never(unreachable)
        except KeyboardInterrupt:
            logger.info("Worker interrupted")
            break
        except Exception as exc:
            logger.critical(traceback.format_exc())
            _m.send_reply(conn, str(exc), 500)
        finally:
            if not event.is_set():
                _t_end = time()
                if logger.is_enabled_for(logger.LogLevel.TRACE):
                    logger.trace(
                        "%s\t%s\tResponse time: %d ms",
                        name,
                        msg.msg_id.name,
                        int((_t_end - _t_start) * 1000.),
                    )
                event.set()
            # Reset feedback
            feedback.reset()


def run_test(conn: Connection, msg: _m.Test, feedback: QgsFeedback):
    """ Feedback test
    """
    done_ts = time() + msg.delay
    canceled = False
    while done_ts > time():
        sleep(1.0)
        canceled = feedback.isCanceled()
        if canceled:
            logger.info("** Test cancelled **")
            break
    if not canceled:
        logger.info("** Test ended without interruption **")
        _m.send_reply(conn, "", 200)
