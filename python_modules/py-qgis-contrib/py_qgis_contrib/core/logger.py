#
# Copyright 2018-2023 3liz
# Author: David Marteau
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
""" Logger
"""
import os
import sys
import logging
from contextlib import contextmanager
from enum import Enum

from typing_extensions import (
    Optional,
    Annotated,
)

from pydantic import (
    Field,
    PlainValidator,
    PlainSerializer,
    WithJsonSchema,
)


from . import config

LOGGER = logging.getLogger('py-qgis-logger')


class LogLevel(Enum):
    NOTSET = logging.NOTSET
    TRACE = logging.DEBUG-1
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    REQ = logging.INFO+1
    RREQ = logging.INFO+2
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


FORMATSTR = '%(asctime)s\t[%(process)d]\t%(levelname)s\t%(message)s'


@config.section('logging')
class LoggingConfig(config.Config):
    level: Annotated[
        LogLevel,
        PlainValidator(lambda v: LogLevel[v.upper()]),
        PlainSerializer(lambda x: x.name, return_type=str),
        WithJsonSchema({
            'enum': [m for m in LogLevel.__members__],
            'type': 'str'
        }),
        Field(default="INFO", validate_default=True)
    ]


def set_log_level(log_level: Optional[LogLevel] = None) -> LogLevel:
    """ Set the log level
    """
    log_level = log_level or config.confservice.conf.logging.level
    LOGGER.setLevel(log_level.value)
    return log_level


def setup_log_handler(
    log_level: Optional[LogLevel] = None,
    channel: Optional[logging.Handler] = None,
):
    """ Initialize log handler with the given log level
    """
    logging.addLevelName(LogLevel.TRACE.value, LogLevel.TRACE.name)
    logging.addLevelName(LogLevel.REQ.value, LogLevel.REQ.name)
    logging.addLevelName(LogLevel.RREQ.value, LogLevel.RREQ.name)

    set_log_level(log_level)

    formatter = logging.Formatter(FORMATSTR)
    channel = channel or logging.StreamHandler(sys.stderr)
    channel.setFormatter(formatter)

    LOGGER.addHandler(channel)


@contextmanager
def logfile_context(workdir: str, basename: str):
    """ Add a temporary file handler
    """
    logfile = os.path.join(workdir, "%s.log" % basename)
    channel = logging.FileHandler(logfile)
    formatter = logging.Formatter(FORMATSTR)
    channel.setFormatter(formatter)
    LOGGER.addHandler(channel)
    try:
        yield
    finally:
        LOGGER.removeHandler(channel)
        channel.close()


#
# Shortcuts
#
warning = LOGGER.warning
info = LOGGER.info
error = LOGGER.error
critical = LOGGER.critical
debug = LOGGER.debug


def trace(msg, *args, **kwargs):
    LOGGER.log(LogLevel.TRACE.value, msg, *args, **kwargs)


def log_req(msg, *args, **kwargs):
    LOGGER.log(LogLevel.REQ.value, msg, *args, **kwargs)


def log_rreq(msg, *args, **kwargs):
    LOGGER.log(LogLevel.RREQ.value, msg, *args, **kwargs)


def isEnabledFor(level: LogLevel):
    return LOGGER.isEnabledFor(level.value)
