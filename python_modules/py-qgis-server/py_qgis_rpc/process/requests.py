""" Qgis server request handler
"""
import traceback

from contextlib import contextmanager
from time import time

import psutil

from typing_extensions import Dict, Optional

from qgis.core import QgsFeedback
from qgis.PyQt.QtCore import QBuffer, QByteArray, QIODevice
from qgis.server import QgsServerRequest, QgsServerResponse

from py_qgis_contrib.core import logger

from . import messages as _m


def _to_qgis_method(method: _m.HTTPMethod) -> QgsServerRequest.Method:
    match method:
        case _m.HTTPMethod.GET:
            return QgsServerRequest.GetMethod
        case _m.HTTPMethod.HEAD:
            return QgsServerRequest.HeadMethod
        case _m.HTTPMethod.POST:
            return QgsServerRequest.PostMethod
        case _m.HTTPMethod.PUT:
            return QgsServerRequest.PutMethod
        case _m.HTTPMethod.DELETE:
            return QgsServerRequest.DeleteMethod
        case _m.HTTPMethod.PATCH:
            return QgsServerRequest.PatchMethod
        case _:
            # Other methods are not implemented
            # in QgisServerRequest
            raise ValueError(method.name)


class Request(QgsServerRequest):

    def __init__(
        self,
        url: str,
        method: QgsServerRequest.Method,
        headers: Dict[str, str],
        data: Optional[bytes],
    ):
        self._data = data
        super().__init__(url, method, headers=headers)

    def data(self) -> QByteArray:
        """ Override
        """
        # Make sure that data is valid
        return QByteArray(self._data) if self._data else QByteArray()


# Define default chunk size to be 1Mo
DEFAULT_CHUNK_SIZE = 1024 * 1024


class Response(QgsServerResponse):
    """ Adaptor to handler response

        The data is written at 'flush()' call.
    """

    def __init__(
            self,
            conn: _m.Connection,
            co_status: Optional[int] = None,
            headers: Optional[Dict] = None,
            chunk_size: int = DEFAULT_CHUNK_SIZE,
            _process: Optional[psutil.Process] = None,
            cache_id: str = "",
            feedback: Optional[QgsFeedback] = None,
    ):
        super().__init__()
        self._buffer = QBuffer()
        self._buffer.open(QIODevice.ReadWrite)
        self._finish = False
        self._conn = conn
        self._status_code = 200
        self._header_written = False
        self._headers: Dict[str, str] = {}
        self._co_status = co_status
        self._process = _process
        self._timestamp = time()
        self._extra_headers: Dict[str, str] = headers or {}
        self._chunk_size = chunk_size
        self._cache_id = cache_id
        self._feedback = feedback

        if self._process:
            self._memory = self._process.memory_info().vms

    def _send_report(self):
        """ Send a request report
            after the last chunk of data
        """
        if not self._process:
            return

        memory = self._process.memory_info().vms - self._memory

        logger.trace(">>> Sending request report")
        _m.send_report(
            self._conn,
            _m.RequestReport(
                memory=memory,
                timestamp=self._timestamp,
                duration=time() - self._timestamp,
            ),
        )

    # Since 3.36
    def feedback(self) -> Optional[QgsFeedback]:
        return self._feedback

    def setStatusCode(self, code: int) -> None:
        if not self._header_written:
            self._status_code = code
        else:
            logger.error("Cannot set status code after header written")

    def statusCode(self) -> int:
        return self._status_code

    def finish(self) -> None:
        """ Terminate the request
        """
        self._finish = True
        self.flush()

    def _send_response(self):
        """ Send response
        """
        self._headers.update(self._extra_headers)

        # Return reply
        _m.send_reply(
            self._conn,
            _m.RequestReply(
                status_code=self._status_code,
                headers=self._headers,
                checkout_status=self._co_status,
                cache_id=self._cache_id,
            ),
        )
        self._header_written = True

    @contextmanager
    def _error(self):
        try:
            yield
        except Exception:
            logger.critical(traceback.format_exc())
            self.sendError(500)

    def flush(self) -> None:
        """ Write the data to the queue
            and flush the socket

            Headers will be written at the first call to flush()
        """
        self._buffer.seek(0)
        bytes_avail = self._buffer.bytesAvailable()

        if self._finish and bytes_avail and not self._header_written:
            # Make sure that we have Content-length set
            self._headers['Content-Length'] = f"{bytes_avail}"

        if not self._header_written:
            # Send response
            self._send_response()

        # Send data as chunks
        data = memoryview(self._buffer.data())
        MAX_CHUNK_SIZE = self._chunk_size
        chunks = (data[i:i + MAX_CHUNK_SIZE] for i in range(0, bytes_avail, MAX_CHUNK_SIZE))
        for chunk in chunks:
            logger.trace("Sending chunk of %s bytes", len(chunk))
            _m.send_chunk(self._conn, chunk)

        if self._finish:
            # Send sentinel to signal end of data
            logger.trace("Sending final chunk")
            _m.send_chunk(self._conn, b'')
            # Send final report
            self._send_report()

        self._buffer.buffer().clear()

    def header(self, key: str) -> str:
        return self._headers.get(key) or ""

    def headers(self) -> Dict[str, str]:
        return self._headers

    def io(self) -> QIODevice:
        return self._buffer

    def data(self) -> QByteArray:
        return self._buffer.data()

    def setHeader(self, key: str, value: str) -> None:
        if not self._header_written:
            self._headers[key] = value
        else:
            logger.error("Cannot set header after header written")

    def removeHeader(self, key: str) -> None:
        self._headers.pop(key, None)

    def sendError(self, code: int, message: Optional[str] = None) -> None:
        try:
            if not self._header_written:
                logger.error("Qgis server error: %s (%s)", message, code)
                self._status_code = code
                self.truncate()
                self._buffer.write(message.encode() if message else b"")
                self.flush()
            else:
                logger.error("Cannot set error after header written")
        except Exception:
            logger.critical("Unrecoverable exception:\n%s", traceback.format_exc())

    def clear(self) -> None:
        self._headers = {}
        self.truncate()

    def headersSent(self) -> bool:
        return self._header_written

    def truncate(self) -> None:
        """ Truncate buffer
        """
        self._buffer.seek(0)
        self._buffer.buffer().clear()
