#
# Copyright 2018-2023 3liz
#

""" Start qgis application
"""
import os
import sys
import logging

from typing import Dict

from . import logger


def setup_qgis_paths(prefix: str) -> None:
    """ Init qgis paths
    """
    qgis_pluginpath = os.path.join(
        prefix,
        os.getenv('QGIS3_PLUGINPATH', '/usr/share/qgis/python/plugins/'),
    )
    sys.path.append(qgis_pluginpath)


# We need to keep a reference instance of the qgis_application object
# and not make this object garbage collected
qgis_application = None


def exit_qgis_application():
    global qgis_application
    if qgis_application:
        # print("\nTerminating Qgis application", file=sys.stderr, flush=True)
        qgis_application.exitQgis()
        qgis_application = None


def setup_qgis_application(
    cleanup: bool = True,
    logprefix: str = 'Qgis:',
    settings: Dict = None,
) -> 'qgis.core.QgsApplication':   # noqa: F821
    """ Start qgis application

         :param boolean cleanup: Register atexit hook to close qgisapplication on exit().
             Note that prevents qgis to segfault when exiting. Default to True.
    """
    global qgis_application
    assert qgis_application is None, "Qgis application already initialized"

    os.environ['QGIS_NO_OVERRIDE_IMPORT'] = '1'
    os.environ['QGIS_DISABLE_MESSAGE_HOOKS'] = '1'

    qgis_prefix = os.environ.get('QGIS3_HOME', '/usr')
    setup_qgis_paths(qgis_prefix)

    from qgis.core import Qgis, QgsApplication

    if Qgis.QGIS_VERSION_INT < 30000:
        raise RuntimeError(f"You need QGIS3 (found {Qgis.QGIS_VERSION_INT})")

    logger.info("Starting Qgis application: %s", Qgis.QGIS_VERSION)

    #  We MUST set the QT_QPA_PLATFORM to prevent
    #  Qt trying to connect to display in containers
    display = os.environ.get('DISPLAY')
    if display is None:
        logger.info("Setting offscreen mode")
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    else:
        logger.info(f"Using DISPLAY: {display}")

    # XXX Set QGIS_PREFIX_PATH, it seems that setPrefixPath
    # does not do the job correctly
    os.environ['QGIS_PREFIX_PATH'] = qgis_prefix

    qgis_application = QgsApplication([], False)
    qgis_application.setPrefixPath(qgis_prefix, True)

    if cleanup:
        # Closing QgsApplication on exit will
        # prevent our app to segfault on exit()
        import atexit

        logger.info(f"{logprefix} Installing cleanup hook")

        @atexit.register
        def exitQgis():
            exit_qgis_application()

    if settings:
        # Initialize settings
        from qgis.core import QgsSettings
        qgsettings = QgsSettings()
        for k, v in settings.items():
            qgsettings.setValue(k, v)

    # Install logger hook
    install_logger_hook(logprefix, )

    print_qgis_version()

    if logger.isEnabledFor(logger.LogLevel.DEBUG):
        logger.debug(qgis_application.showSettings())

    logger.info(f"{logprefix} Qgis application configured......")

    return qgis_application


def install_logger_hook(logprefix: str) -> None:
    """ Install message log hook
    """
    from qgis.core import Qgis, QgsApplication
    # Add a hook to qgis  message log

    def writelogmessage(message, tag, level):
        arg = f'{logprefix} {tag}: {message}'
        if level == Qgis.Warning:
            logger.warning(arg)
        elif level == Qgis.Critical:
            logger.error(arg)
        elif os.getenv("QGIS_LOG_DEBUG_VERBOSE", "0") == "1":
            # Qgis is somehow very noisy
            # log only if verbose is set
            logger.debug(arg)

    messageLog = QgsApplication.messageLog()
    messageLog.messageReceived.connect(writelogmessage)


def init_qgis_application():
    setup_qgis_application()

    from qgis.PyQt.QtCore import QCoreApplication
    from qgis.core import QgsApplication

    # From qgis server
    # Will enable us to read qgis setting file
    QCoreApplication.setOrganizationName(QgsApplication.QGIS_ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(QgsApplication.QGIS_ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(QgsApplication.QGIS_APPLICATION_NAME)

    qgis_application.initQgis()

    optpath = os.getenv('QGIS_OPTIONS_PATH')
    if optpath:
        # Log qgis settings
        load_qgis_settings(optpath, logger)


def init_qgis_processing(**kwargs) -> None:
    """ Initialize processing
    """
    # We need to fully initialize Qgis
    #
    # This is not needed when initializing
    # A QgsServer instance because the initialization
    # processs handle things under the hood
    init_qgis_application(**kwargs)

    from processing.core.Processing import Processing
    from qgis.analysis import QgsNativeAlgorithms
    from qgis.core import QgsApplication

    # Update the network configuration
    # XXX: At the time the settings are read, the networkmanager is already
    # initialized, but with the wrong settings
    set_proxy_configuration(logger)

    if logger.isEnabledFor(logging.DEBUG):
        print(qgis_application.showSettings())

    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    Processing.initialize()


def init_qgis_server(**kwargs) -> 'qgis.server.QgsServer':  # noqa: F821
    """ Init Qgis server
    """
    setup_qgis_application(**kwargs)

    from qgis.server import QgsServer
    server = QgsServer()

    # Update the network configuration
    # XXX: At the time the settings are read, the neworkmanager is already
    # initialized, but with the wrong settings
    set_proxy_configuration(logger)

    return server


def load_qgis_settings(optpath, logger):
    """ Load qgis settings
    """
    from qgis.PyQt.QtCore import QSettings
    from qgis.core import QgsSettings

    QSettings.setDefaultFormat(QSettings.IniFormat)
    QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, optpath)
    logger.info("Settings loaded from %s", QgsSettings().fileName())


def set_proxy_configuration() -> None:
    """ Display proxy configuration
    """
    from qgis.PyQt.QtNetwork import QNetworkProxy
    from qgis.core import QgsNetworkAccessManager

    nam = QgsNetworkAccessManager.instance()
    nam.setupDefaultProxyAndCache()

    proxy = nam.fallbackProxy()
    proxy_type = proxy.type()
    if proxy_type == QNetworkProxy.NoProxy:
        return

    logger.info(
        "QGIS Proxy configuration enabled: %s:%s, type: %s",
        proxy.hostName(), proxy.port(),
        {
            QNetworkProxy.DefaultProxy: 'DefaultProxy',
            QNetworkProxy.Socks5Proxy: 'Socks5Proxy',
            QNetworkProxy.HttpProxy: 'HttpProxy',
            QNetworkProxy.HttpCachingProxy: 'HttpCachingProxy',
            QNetworkProxy.HttpCachingProxy: 'FtpCachingProxy',
        }.get(proxy_type, 'Undetermined')
    )  # noqa E124


def print_qgis_version(verbose: bool = False) -> None:
    """ Output the qgis version
    """
    from qgis.core import Qgis

    if Qgis.QGIS_VERSION_INT < 32200:
        print(f"QGIS {Qgis.QGIS_VERSION} '{Qgis.QGIS_RELEASE_NAME}' ({Qgis.QGIS_VERSION_INT})")
    else:
        from qgis.core import QgsCommandLineUtils
        print(QgsCommandLineUtils.allVersions())

    if verbose:
        init_qgis_application()
        print(qgis_application.showSettings())
        sys.exit(1)
