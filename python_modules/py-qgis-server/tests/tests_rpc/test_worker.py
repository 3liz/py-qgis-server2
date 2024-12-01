import asyncio  # noqa

from contextlib import asynccontextmanager
from time import time

import pytest

from py_qgis_rpc import messages
from py_qgis_rpc.worker import Worker
from py_qgis_rpc.config import ProjectsConfig, WorkerConfig

pytest_plugins = ('pytest_asyncio',)


@asynccontextmanager
async def worker_context(projects: ProjectsConfig):
    worker = Worker(WorkerConfig(name="Test", projects=projects))
    await worker.start()
    try:
        yield worker
    finally:
        print("Sending Quit message")
        await worker.quit()
        assert not worker.is_alive


async def test_worker_io(projects: ProjectsConfig):
    """ Test worker process
    """
    async with worker_context(projects) as worker:

        # Test ping message
        status, _ = await worker.io.send_message(messages.PingMsg())
        assert status == 200

        # Test ping message as dict
        status, resp = await worker.io.send_message(
            {'msg_id': messages.MsgType.PING, 'echo': "hello"},
        )
        assert status == 200
        assert resp == "hello"

        # Test Qgis server OWS request with valid project
        status, resp = await worker.io.send_message(
            messages.OwsRequestMsg(
                service="WFS",
                request="GetCapabilities",
                target="/france/france_parts",
                url="http://localhost:8080/test.3liz.com",
                debug_report=True,
            ),
        )

        print("test_worker_io::status", status)

        assert status == 200
        assert resp.status_code == 200

        print(f"> {resp.chunked}")
        print(f"> {resp.headers}")

        if resp.chunked:
            # Stream remaining bytes
            async for chunk in worker.io.stream_bytes():
                assert len(chunk > 0)

        # Get final report
        report = await worker.io.read_report()
        print(f"> {report.memory}")
        print(f"> {report.timestamp}")
        print(f"> {report.duration}")


async def test_chunked_response(projects: ProjectsConfig):
    """ Test Response with chunk
    """
    async with worker_context(projects) as worker:

        status, _ = await worker.io.send_message(messages.PingMsg())
        assert status == 200

        start = time()
        # Test Qgis server OWS request with valid project
        status, resp = await worker.io.send_message(
            messages.OwsRequestMsg(
                service="WFS",
                request="GetFeature",
                version="1.0.0",
                options="TYPENAME=france_parts_bordure",
                target="/france/france_parts",
                url="http://localhost:8080/test.3liz.com",
                debug_report=True,
            ),
        )

        total_time = time() - start
        print("> ", total_time)
        assert status == 200
        assert resp.status_code == 200

        print("> chunked", resp.chunked)
        print("> headers", resp.headers)

        if resp.chunked:
            # Stream remaining bytes
            async for chunk in worker.io.stream_bytes():
                assert len(chunk) > 0

        # Get final report
        report = await worker.io.read_report()
        print("> ", report.memory)
        print("> ", report.timestamp)
        print("> ", report.duration)
        print("> overhead:", total_time - report.duration)


async def test_cache_api(projects: ProjectsConfig):
    """ Test worker cache api
    """
    async with worker_context(projects) as worker:

        # Pull
        status, resp = await worker.io.send_message(
            messages.CheckoutProjectMsg(uri="/france/france_parts", pull=True),
        )
        assert status == 200
        assert resp.status == messages.CheckoutStatus.NEW
        assert resp.pinned

        uri = resp.uri

        # Checkout
        status, resp = await worker.io.send_message(
            messages.CheckoutProjectMsg(uri="/france/france_parts", pull=False),
        )
        assert status == 200
        assert resp.status == messages.CheckoutStatus.UNCHANGED

        # List
        status, resp = await worker.io.send_message(
            messages.ListCacheMsg(),
        )

        assert status == 200
        assert resp == 1
        status, _item = await worker.io.read_message()
        while status == 206:
            status, _item = await worker.io.read_message()
        assert status == 200

        # Project info
        status, resp = await worker.io.send_message(
            messages.GetProjectInfoMsg(uri="/france/france_parts"),
        )
        assert status == 200

        # Drop project
        status, resp = await worker.io.send_message(
            messages.DropProjectMsg(uri=uri),
        )
        assert status == 200

        # Empty List
        status, resp = await worker.io.send_message(
            messages.ListCacheMsg(),
        )

        assert status == 200
        assert resp == 0


async def test_catalog(projects: ProjectsConfig):
    """ Test worker cache api
    """
    async with worker_context(projects) as worker:

        # Pull
        status, _resp = await worker.io.send_message(
            messages.CatalogMsg(location="/france"),
        )
        assert status == 200
        status, item = await worker.io.read_message()
        count = 0
        while status == 206:
            count += 1
            print("ITEM", item.uri)
            status, item = await worker.io.read_message()
        assert status == 200
        assert count == 3


async def test_ows_request(projects: ProjectsConfig):
    """ Test worker process
    """
    async with worker_context(projects) as worker:

        echo = await worker.ping("hello")
        assert echo == "hello"

        # Test Qgis server OWS request with valid project
        resp, stream = await worker.ows_request(
            service="WFS",
            request="GetCapabilities",
            target="/france/france_parts",
            url="http://localhost:8080/test.3liz.com",
        )

        assert resp.status_code == 200
        print(f"> {resp.chunked}")
        print(f"> {resp.headers}")

        # Stream remaining bytes
        if stream:
            async for chunk in stream:
                assert len(chunk) > 0


async def test_ows_chunked_request(projects: ProjectsConfig):
    """ Test worker process
    """
    async with worker_context(projects) as worker:

        echo = await worker.ping("hello")
        assert echo == "hello"

        # Test Qgis server OWS request with valid project
        resp, stream = await worker.ows_request(
            service="WFS",
            request="GetFeature",
            version="1.0.0",
            options="TYPENAME=france_parts_bordure",
            target="/france/france_parts",
            url="http://localhost:8080/test.3liz.com",
        )

        assert resp.status_code == 200
        print(f"> {resp.chunked}")
        print(f"> {resp.headers}")

        assert resp.chunked
        assert stream is not None
        # Stream remaining bytes
        async for chunk in stream:
            assert len(chunk) > 0

        with pytest.raises(TimeoutError):
            async with asyncio.timeout(1):
                _ = await worker.io.read_bytes()


async def test_api_request(projects: ProjectsConfig):
    """ Test worker process
    """
    async with worker_context(projects) as worker:

        echo = await worker.ping("hello")
        assert echo == "hello"

        # Test Qgis server API request with valid project
        resp, stream = await worker.api_request(
            name="WFS3",
            path="/collections",
            target="/france/france_parts",
            url="http://localhost:8080/features",
        )

        assert resp.status_code == 200
        print(f"> {resp.chunked}")
        print(f"> {resp.headers}")

        # Stream remaining bytes
        if stream:
            async for chunk in stream:
                assert len(chunk) > 0
