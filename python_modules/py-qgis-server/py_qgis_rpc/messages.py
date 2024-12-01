""" Messages for communicating with the qgis server
    sub process
"""
import pickle  # nosec

from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from pathlib import Path

from pydantic import BaseModel, Field, JsonValue, TypeAdapter
from typing_extensions import (
    Annotated,
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Type,
    Union,
)

from py_qgis_cache import CheckoutStatus
from py_qgis_contrib.core.qgis import PluginType


class MsgType(IntEnum):
    PING = 1
    QUIT = 2
    REQUEST = 3
    OWSREQUEST = 4
    APIREQUEST = 5
    CHECKOUT_PROJECT = 6
    DROP_PROJECT = 7
    CLEAR_CACHE = 8
    LIST_CACHE = 9
    UPDATE_CACHE = 10
    PROJECT_INFO = 11
    PLUGINS = 12
    CATALOG = 13
    PUT_CONFIG = 14
    GET_CONFIG = 15
    ENV = 16
    STATS = 17
    TEST = 18

# Note: HTTPMethod is defined in python 3.11 via http module


class HTTPMethod(Enum):
    GET = auto()
    HEAD = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    CONNECT = auto()
    OPTIONS = auto()
    TRACE = auto()
    PATCH = auto()


class MsgModel(BaseModel, frozen=True):
    pass


#
# REQUEST
#
@dataclass(frozen=True)
class RequestReply:
    status_code: int
    data: bytes
    chunked: bool
    checkout_status: Optional[CheckoutStatus]
    headers: Dict[str, str] = field(default_factory=dict)
    cache_id: str = ""


@dataclass(frozen=True)
class RequestReport:
    memory: Optional[int]
    timestamp: float
    duration: float


class OwsRequestMsg(MsgModel):
    msg_id: Literal[MsgType.OWSREQUEST] = MsgType.OWSREQUEST
    service: str
    request: str
    target: str
    url: str
    version: Optional[str] = None
    direct: bool = False
    options: Optional[str] = None
    headers: Dict[str, str] = Field({})
    request_id: str = ""
    debug_report: bool = False


class ApiRequestMsg(MsgModel):
    msg_id: Literal[MsgType.APIREQUEST] = MsgType.APIREQUEST
    name: str
    path: str
    method: HTTPMethod
    url: str = '/'
    data: Optional[bytes] = None
    delegate: bool = False
    target: Optional[str] = None
    direct: bool = False
    options: Optional[str] = None
    headers: Dict[str, str] = Field({})
    request_id: str = ""
    debug_report: bool = False


class RequestMsg(MsgModel):
    msg_id: Literal[MsgType.REQUEST] = MsgType.REQUEST
    url: str
    method: HTTPMethod
    data: Optional[bytes]
    target: Optional[str]
    direct: bool = False
    headers: Dict[str, str] = Field({})
    request_id: str = ""
    debug_report: bool = False


class PingMsg(MsgModel):
    msg_id: Literal[MsgType.PING] = MsgType.PING
    echo: Optional[str] = None


#
# QUIT
#
class QuitMsg(MsgModel):
    msg_id: Literal[MsgType.QUIT] = MsgType.QUIT


@dataclass(frozen=True)
class CacheInfo:
    uri: str
    status: CheckoutStatus
    in_cache: bool
    timestamp: Optional[float] = None
    name: str = ""
    storage: str = ""
    last_modified: Optional[float] = None
    saved_version: Optional[str] = None
    debug_metadata: Dict[str, int] = field(default_factory=dict)
    cache_id: str = ""
    last_hit: float = 0
    hits: int = 0
    pinned: bool = False


#
# PULL_PROJECT
#
class CheckoutProjectMsg(MsgModel):
    msg_id: Literal[MsgType.CHECKOUT_PROJECT] = MsgType.CHECKOUT_PROJECT
    uri: str
    pull: bool = False


#
# DROP_PROJECT
#
class DropProjectMsg(MsgModel):
    msg_id: Literal[MsgType.DROP_PROJECT] = MsgType.DROP_PROJECT
    uri: str


#
# CLEAR_CACHE
#
class ClearCacheMsg(MsgModel):
    msg_id: Literal[MsgType.CLEAR_CACHE] = MsgType.CLEAR_CACHE


#
# LIST_CACHE
#
class ListCacheMsg(MsgModel):
    msg_id: Literal[MsgType.LIST_CACHE] = MsgType.LIST_CACHE
    # Filter by status
    status_filter: Optional[CheckoutStatus] = None


#
# UPDATE_CACHE
#
class UpdateCacheMsg(MsgModel):
    msg_id: Literal[MsgType.UPDATE_CACHE] = MsgType.UPDATE_CACHE


#
# PLUGINS
#
@dataclass(frozen=True)
class PluginInfo:
    name: str
    path: Path
    plugin_type: PluginType
    metadata: JsonValue


class PluginsMsg(MsgModel):
    msg_id: Literal[MsgType.PLUGINS] = MsgType.PLUGINS


#
# PROJECT_INFO
#
@dataclass(frozen=True)
class LayerInfo:
    layer_id: str
    name: str
    source: str
    crs: str
    is_valid: bool
    is_spatial: bool


@dataclass(frozen=True)
class ProjectInfo:
    status: CheckoutStatus
    uri: str
    filename: str
    crs: str
    last_modified: float
    storage: str
    has_bad_layers: bool
    layers: List[LayerInfo]
    cache_id: str = ""


class GetProjectInfoMsg(MsgModel):
    msg_id: Literal[MsgType.PROJECT_INFO] = MsgType.PROJECT_INFO
    uri: str


#
# CONFIG
#
class GetConfigMsg(MsgModel):
    msg_id: Literal[MsgType.GET_CONFIG] = MsgType.GET_CONFIG


class PutConfigMsg(MsgModel):
    msg_id: Literal[MsgType.PUT_CONFIG] = MsgType.PUT_CONFIG
    config: Optional[Dict] = None


#
# CATALOG
#
@dataclass(frozen=True)
class CatalogItem:
    uri: str
    name: str
    storage: str
    last_modified: float
    public_uri: str


class CatalogMsg(MsgModel):
    msg_id: Literal[MsgType.CATALOG] = MsgType.CATALOG
    location: Optional[str] = None


#
# ENV
#
class GetEnvMsg(MsgModel):
    msg_id: Literal[MsgType.ENV] = MsgType.ENV


#
# TEST
#
class TestMsg(MsgModel):
    msg_id: Literal[MsgType.TEST] = MsgType.TEST
    delay: int

#
# Asynchronous Pipe connection reader
#


@dataclass(frozen=True)
class Envelop:
    status: int
    msg: Any


Message = Annotated[
    Union[
        OwsRequestMsg,
        ApiRequestMsg,
        RequestMsg,
        PingMsg,
        QuitMsg,
        CheckoutProjectMsg,
        DropProjectMsg,
        ClearCacheMsg,
        ListCacheMsg,
        UpdateCacheMsg,
        PluginsMsg,
        GetProjectInfoMsg,
        GetConfigMsg,
        PutConfigMsg,
        CatalogMsg,
        GetEnvMsg,
        TestMsg,
    ],
    Field(discriminator="msg_id"),
]


MessageAdapter: TypeAdapter[Message] = TypeAdapter(Message)


class Connection(Protocol):
    def recv(self) -> Message: ...
    def send_bytes(self, data: bytes): ...


def send_reply(conn: Connection, msg: Any, status: int = 200):  # noqa ANN401
    """  Send a reply in a envelope message """
    conn.send_bytes(pickle.dumps(Envelop(status, msg=msg)))


def send_report(conn: Connection, report: RequestReport):
    """ Send report """
    conn.send_bytes(pickle.dumps(report))


#
# XXX Note that data sent by child *MUST* be retrieved in parent
# side, otherwise cpu goes wild.


def cast_into[T](o: Any, t: Type[T]) -> T:  # noqa ANN401
    if not isinstance(o, t):
        raise ValueError(f"Cast failed, Expecting {t}, not {type(o)}")
    return o



