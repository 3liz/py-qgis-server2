""" gRPC Client test
"""
from typing import (
    Optional,
    List,
)
from contextlib import contextmanager
from pathlib import Path
from time import time, sleep
import json
import click
import sys
import os
import grpc
from .._grpc import api_pb2
from .._grpc import api_pb2_grpc

from grpc_health.v1 import health_pb2       # HealthCheckRequest
from grpc_health.v1 import health_pb2_grpc  # HealthStub


from google.protobuf import json_format


def MessageToJson(msg) -> str:
    return json_format.MessageToJson(
        msg,
        including_default_value_fields=True,
    )


@contextmanager
def connect(
    stub=None,
    use_ssl: bool = False,
):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    #
    # For more channel options, please see https://grpc.io/grpc/core/group__grpc__arg__keys.html
    with grpc.insecure_channel(
        target=os.getenv("QGIS_GRPC_HOST", "localhost:23456"),
        options=[
            ("grpc.lb_policy_name", "round_robin"),
            ("grpc.enable_retries", 1),
            ("grpc.keepalive_timeout_ms", 10000),
        ],
    ) as channel:
        try:
            stub = stub or api_pb2_grpc.QgisAdminStub
            yield stub(channel)
            # Timeout in seconds.
            # Please refer gRPC Python documents for more detail. https://grpc.io/grpc/python/grpc.html
        except grpc.RpcError as rpcerr:
            print("RPC ERROR:", rpcerr.code(), rpcerr.details(), file=sys.stderr)
            print_metadata(rpcerr.initial_metadata())
            print_metadata(rpcerr.trailing_metadata())


def print_metadata(metadata):
    status_code = ""
    for k, v in metadata:
        if k == "x-reply-status-code":
            status_code = v
        elif k.startswith("x-reply-header-"):
            h = k.replace("x-reply-header-", "", 1)
            print(h.title(), ":", v, file=sys.stderr)
        elif k.startswith("x-"):
            print(k, ":", v, file=sys.stderr)
    if status_code:
        print("Return code:", status_code, file=sys.stderr)


@click.group('commands')
def cli_commands():
    pass


@cli_commands.group('request')
def request_commands():
    """ Commands for requesting qgis server
    """
    pass


@request_commands.command("ows")
@click.argument('project', nargs=1)
@click.option("--service", help="OWS service name", required=True)
@click.option("--request", help="OWS request name", required=True)
@click.option("--version", help="OWS service version")
@click.option("--param", "-p", multiple=True, help="Parameters KEY=VALUE")
@click.option("--headers", "-H", is_flag=True, help="Show headers")
@click.option("--url", help="Origin url")
@click.option(
    "--output", "-o",
    help="Destination file",
    type=click.Path(dir_okay=False),
)
def ows_request(
    project: str,
    service: str,
    request: str,
    version: Optional[str],
    param: List[str],
    headers: bool,
    output: Optional[str],
    url: Optional[str],
):
    """ Send OWS request
    """
    with connect(api_pb2_grpc.QgisServerStub) as stub:
        _t_start = time()
        stream = stub.ExecuteOwsRequest(
            api_pb2.OwsRequest(
                service=service,
                request=request,
                target=project,
                url=url or "",
            ),
            timeout=10,
        )

        chunk = next(stream)
        _t_end = time()

        fp = Path(output).open("w") if output else sys.stdout
        print(chunk, file=fp)
        for chunk in stream:
            print(chunk, file=fp)

        if headers:
            print_metadata(stream.initial_metadata())

        _t_ms = int((_t_end - _t_start) * 1000.0)
        print("First chunk returned in", _t_ms, "ms", file=sys.stderr)


@cli_commands.group('cache')
def cache_commands():
    """ Commands for cache management
    """
    pass


@cache_commands.command("checkout")
@click.argument('project', nargs=1)
@click.option('--pull', is_flag=True, help="Load project in cache")
def checkout_project(project: str, pull: bool):
    """ CheckoutProject PROJECT from cache
    """
    with connect() as stub:
        stream = stub.CheckoutProject(
            api_pb2.CheckoutRequest(uri=project, pull=pull)
        )
        count = 0
        for item in stream:
            count += 1
            print(MessageToJson(item))

        print(f"Returned {count} items", file=sys.stderr)


@cache_commands.command("drop")
@click.argument('project', nargs=1)
def drop_project(project: str):
    """ Drop PROJECT from cache
    """
    with connect() as stub:
        stream = stub.DropProject(
            api_pb2.DropRequest(uri=project)
        )
        count = 0
        for item in stream:
            count += 1
            print(MessageToJson(item))

        print(f"Returned {count} items", file=sys.stderr)


@cache_commands.command("clear")
def clear_cache():
    """ Clear cache
    """
    with connect() as stub:
        stub.ClearCache(
            api_pb2.Empty()
        )


@cache_commands.command("list")
@click.option("--status", help="Status filter")
def list_cache(status: str):
    """ List projects from cache
    """
    with connect() as stub:
        stream = stub.ListCache(
            api_pb2.ListRequest(status_filter=status)
        )

        for k, v in stream.initial_metadata():
            if k == "x-reply-header-cache-count":
                print("Cache size:", v, file=sys.stderr)

        for item in stream:
            print(MessageToJson(item))


@cache_commands.command("update")
def update_cache():
    """ List projects from cache
    """
    with connect() as stub:
        stream = stub.UpdateCache(api_pb2.Empty())
        for item in stream:
            print(MessageToJson(item))


@cache_commands.command("info")
@click.argument('project', nargs=1)
def project_info(project: str):
    """ Return info from PROJECT in cache
    """
    with connect() as stub:
        stream = stub.GetProjectInfo(
            api_pb2.ProjectRequest(uri=project)
        )
        count = 0
        for item in stream:
            count += 1
            print(MessageToJson(item))

        print(f"Returned {count} items", file=sys.stderr)


@cache_commands.command("catalog")
@click.option('--location', help="Select location")
def catalog(location: Optional[str]):
    """ List projects from cache
    """
    with connect() as stub:
        stream = stub.Catalog(
            api_pb2.CatalogRequest(location=location)
        )
        count = 0
        for item in stream:
            count += 1
            print(MessageToJson(item))

        print(f"Returned {count} items", file=sys.stderr)

#
# Plugins
#


@cli_commands.group('plugin')
def plugin_commands():
    """ Commands for cache management
    """
    pass


@plugin_commands.command("list")
def list_plugins():
    """ List projects from cache
    """
    import json
    with connect() as stub:
        stream = stub.ListPlugins(
            api_pb2.Empty()
        )

        for k, v in stream.initial_metadata():
            if k == "x-reply-header-installed-plugins":
                print("Installed plugins:", v, file=sys.stderr)

        for item in stream:
            print(
                json.dumps(
                    dict(
                        name=item.name,
                        path=item.path,
                        pluginType=item.plugin_type,
                        metadata=json.loads(item.json_metadata),
                    ),
                    indent=4,
                )
            )


#
# Config
#
@cli_commands.group('config')
def config_commands():
    """ Commands for cache management
    """
    pass


@config_commands.command("get")
def get_config():
    """ Get server configuration
    """
    with connect() as stub:
        resp = stub.GetConfig(api_pb2.Empty())
        print(resp.json)


@config_commands.command("set")
@click.argument('config', nargs=1)
def set_config(config: str):
    """ Send CONFIG to remote
    """
    with connect() as stub:
        if config.startswith('@'):
            config = Path(config[1:]).open().read()

        # Validate as json
        try:
            json.loads(config)
            stub.SetConfig(api_pb2.JsonConfig(json=config))
        except json.JSONDecodeError as err:
            print(err, file=sys.stderr)


#
#  status
#

@cli_commands.group('status')
def status_commands():
    """ Commands for cache management
    """
    pass


@status_commands.command("env")
def get_status_env():
    """ Get environment status
    """
    with connect() as stub:
        resp = stub.GetEnv(api_pb2.Empty())
        print(resp.json)


@status_commands.command("disable")
def disable_server():
    """ Disable server serving stats
    """
    with connect() as stub:
        _ = stub.SetServerServingStatus(
            api_pb2.ServerStatus(status=api_pb2.ServingStatus.NOT_SERVING),
        )


@status_commands.command("enable")
def enable_server():
    """ Enable server serving stats
    """
    with connect() as stub:
        _ = stub.SetServerServingStatus(
            api_pb2.ServerStatus(status=api_pb2.ServingStatus.SERVING),
        )


@cli_commands.command("ping")
@click.option("--count", default=1, help="Number of requests to send")
@click.option("--server", is_flag=True, help="Ping qgis server service")
def ping(count: int, server: bool = False):
    """ Get environment status
    """
    stub = api_pb2_grpc.QgisServerStub if server else None
    target = "server" if server else "admin"
    with connect(stub) as stub:
        for n in range(count):
            _t_start = time()
            resp = stub.Ping(api_pb2.PingRequest(echo=str(n)))
            _t_end = time()
            print(
                f"({target}) ",
                f"seq={n:<5} resp={resp.echo:<5} time={int((_t_end-_t_start) * 1000.)} ms",
            )
            sleep(1)


@cli_commands.command("healthcheck")
@click.option("--watch", "-w", is_flag=True, help="Watch status changes")
@click.option("--server", is_flag=True, help="Check qgis server service")
def healthcheck_status(watch: bool, server: bool):
    """ Check the status of a GRPC server
    """
    target = "QgisServer" if server else "QgisAdmin"
    with connect(stub=health_pb2_grpc.HealthStub) as stub:
        ServingStatus = health_pb2.HealthCheckResponse.ServingStatus
        request = health_pb2.HealthCheckRequest(service=target)
        if watch:
            for resp in stub.Watch(request):
                print(f"{target}:", ServingStatus.Name(resp.status))
        else:
            resp = stub.Check(request)
            print(f"{target}", ServingStatus.Name(resp.status))


@cli_commands.command("stats")
@click.option("--watch", "-w", is_flag=True, help="Watch mode")
@click.option(
    "--interval", "-i",
    default=1,
    help="Interval in seconds in watch mode",
)
def display_stats(watch: bool, interval: int):
    """ Check the status of a GRPC server
    """
    with connect() as stub:
        resp = stub.Stats(api_pb2.Empty())
        print(MessageToJson(resp))
        if watch:
            resp = stub.Stats(api_pb2.Empty())
            print(MessageToJson(resp))
            sleep(interval)


cli_commands()
