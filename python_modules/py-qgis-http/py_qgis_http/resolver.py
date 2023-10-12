""" Dns resolver
"""
import ipaddress

from typing_extensions import (
    List,
    Optional,
    Annotated,
    Tuple,
)

from pydantic import (
    Field,
    AfterValidator,
    PlainValidator,
    PlainSerializer,
    WithJsonSchema,
    StringConstraints,
)

from pathlib import PurePosixPath

from py_qgis_contrib.core.config import (
    Config,
    SSLConfig,
)

DEFAULT_PORT = 23456

#
# Resolver
#


def _validate_address(v: str | Tuple[str, int]) -> str | Tuple[str, int]:
    """ Validate address

        Address may be:
        * A string `unix:path`
        * A 2-tuple `(name, port)` where `name` is either an ip addresse
          or a hostname
    """
    def _check_ip(addr):
        try:
            addr = addr.strip('[]')
            ipaddr = ipaddress.ip_address(addr)
            if isinstance(ipaddr, ipaddress.IPv6Address):
                addr = f"[{addr}]"
        except ValueError:
            # Assume this is a hostname
            pass
        return addr

    match v:
        case (addr, port):
            return (_check_ip(addr.removeprefix('tcp://')), port)
        case str() as addr if addr.startswith('unix:'):
            return addr
        case str() as addr:
            return (_check_ip(addr.removeprefix('tcp://')), DEFAULT_PORT)
        case _:
            raise ValueError(f"Unmanageable address: {addr}")


NetAddress = Annotated[
    str | Tuple[str, int],
    AfterValidator(_validate_address),
]


def _validate_route(r: str) -> PurePosixPath:
    """ Validate a path:
        * Path must be absolute (i.e start with '/')
    """
    if not isinstance(r, str):
        raise ValueError("Expecting string")
    if not r.startswith('/'):
        raise ValueError("Route must start with a '/'")
    if r.find('/_/') >= 0:
        raise ValueError("Route must not contains the reserved path: '/_/'")
    return PurePosixPath(r)


Route = Annotated[
    PurePosixPath,
    PlainValidator(_validate_route),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({'type': 'str'}),
]


class ApiEndpoint(Config):
    endpoint: str = Field(
        pattern=r"^[^\/]+",
        title="Api endpoint"
    )
    delegate_to: Optional[str] = Field(
        default=None,
        title="Api name to delegate to",
        description=(
            "Api delegation allow for using a baseurl different "
            "from the expected rootpath of qgis server api."
            "For exemple, wfs3 request may be mapped to a completely different "
            "root path. "
        )
    )
    name: str = Field(
        default="",
        title="Descriptive name",
    )
    description: str = Field(
        default="",
        title="Api description",
    )


class BackendConfig(Config):
    title: str = Field(
        default="",
        title="A descriptive title",
    )
    description: str = Field(
        default="",
        title="A description of the service",
    )
    address: NetAddress = Field(
        default=('localhost', DEFAULT_PORT),
        title="Remote address of the service",
        description=_validate_address.__doc__,
    )

    ssl: Optional[SSLConfig] = None

    # Define route to service
    route: Route = Field(title="Route to service")

    # Specific timeout
    timeout: int = Field(
        default=20,
        title="Request timeout",
        description=(
            "Set the timeout for Qgis response in seconds. "
            "If a Qgis worker takes more than the corresponding value "
            "a timeout error (504) is returned to the client."
        ),
    )

    forward_headers: List[Annotated[str, StringConstraints(to_lower=True)]] = Field(
        default=['x-qgis-*', 'x-lizmap-*'],
        title="Define headers that will be forwarded to Qgis server backend",
        description=(
            "Set the headers that will be forwarded to the Qgis server backend. "
            "This may be useful if you have plugins that may deal with request headers."
        ),
    )

    api: List[ApiEndpoint] = Field(
        default=[],
        title="Api endpoints",
    )

    allow_direct_resolution: bool = Field(
        default=False,
        title="Allow direct path resolution",
        description=(
            "Allow remote worker to use direct project path resolution. "
            "WARNING: allowing this may be a security vulnerabilty. "
            "See worker configuration for details."
        )
    )

    getfeature_limit: Optional[Annotated[int, Field(gt=0)]] = Field(
        default=None,
        title="WFS/GetFeature limit",
        description=(
            "Force setting a limit for WFS/GetFeature requests. "
            "By default Qgis does not set limits and that may cause "
            "issues with large collections."
        )
    )

    def to_string(self) -> str:
        match self.address:
            case (addr, port):
                return f"{addr}:{port}"
            case addr:
                return addr
