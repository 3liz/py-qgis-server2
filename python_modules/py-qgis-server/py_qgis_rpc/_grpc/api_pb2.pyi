from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERVING: _ClassVar[ServingStatus]
    NOT_SERVING: _ClassVar[ServingStatus]
SERVING: ServingStatus
NOT_SERVING: ServingStatus

class PingRequest(_message.Message):
    __slots__ = ("echo",)
    ECHO_FIELD_NUMBER: _ClassVar[int]
    echo: str
    def __init__(self, echo: _Optional[str] = ...) -> None: ...

class PingReply(_message.Message):
    __slots__ = ("echo",)
    ECHO_FIELD_NUMBER: _ClassVar[int]
    echo: str
    def __init__(self, echo: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StatsReply(_message.Message):
    __slots__ = ("num_workers", "stopped_workers", "worker_failure_pressure", "request_pressure", "uptime")
    NUM_WORKERS_FIELD_NUMBER: _ClassVar[int]
    STOPPED_WORKERS_FIELD_NUMBER: _ClassVar[int]
    WORKER_FAILURE_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    UPTIME_FIELD_NUMBER: _ClassVar[int]
    num_workers: int
    stopped_workers: int
    worker_failure_pressure: float
    request_pressure: float
    uptime: int
    def __init__(self, num_workers: _Optional[int] = ..., stopped_workers: _Optional[int] = ..., worker_failure_pressure: _Optional[float] = ..., request_pressure: _Optional[float] = ..., uptime: _Optional[int] = ...) -> None: ...

class ServerStatus(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ServingStatus
    def __init__(self, status: _Optional[_Union[ServingStatus, str]] = ...) -> None: ...

class ResponseChunk(_message.Message):
    __slots__ = ("chunk",)
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    def __init__(self, chunk: _Optional[bytes] = ...) -> None: ...

class OwsRequest(_message.Message):
    __slots__ = ("service", "request", "target", "version", "url", "direct", "options", "request_id", "debug_report")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DIRECT_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DEBUG_REPORT_FIELD_NUMBER: _ClassVar[int]
    service: str
    request: str
    target: str
    version: str
    url: str
    direct: bool
    options: str
    request_id: str
    debug_report: bool
    def __init__(self, service: _Optional[str] = ..., request: _Optional[str] = ..., target: _Optional[str] = ..., version: _Optional[str] = ..., url: _Optional[str] = ..., direct: bool = ..., options: _Optional[str] = ..., request_id: _Optional[str] = ..., debug_report: bool = ...) -> None: ...

class ApiRequest(_message.Message):
    __slots__ = ("name", "path", "method", "data", "delegate", "target", "url", "direct", "options", "request_id", "debug_report")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DELEGATE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DIRECT_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DEBUG_REPORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    path: str
    method: str
    data: bytes
    delegate: bool
    target: str
    url: str
    direct: bool
    options: str
    request_id: str
    debug_report: bool
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., method: _Optional[str] = ..., data: _Optional[bytes] = ..., delegate: bool = ..., target: _Optional[str] = ..., url: _Optional[str] = ..., direct: bool = ..., options: _Optional[str] = ..., request_id: _Optional[str] = ..., debug_report: bool = ...) -> None: ...

class GenericRequest(_message.Message):
    __slots__ = ("url", "method", "data", "target", "direct", "request_id", "debug_report")
    URL_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    DIRECT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DEBUG_REPORT_FIELD_NUMBER: _ClassVar[int]
    url: str
    method: str
    data: bytes
    target: str
    direct: bool
    request_id: str
    debug_report: bool
    def __init__(self, url: _Optional[str] = ..., method: _Optional[str] = ..., data: _Optional[bytes] = ..., target: _Optional[str] = ..., direct: bool = ..., request_id: _Optional[str] = ..., debug_report: bool = ...) -> None: ...

class CheckoutRequest(_message.Message):
    __slots__ = ("uri", "pull")
    URI_FIELD_NUMBER: _ClassVar[int]
    PULL_FIELD_NUMBER: _ClassVar[int]
    uri: str
    pull: bool
    def __init__(self, uri: _Optional[str] = ..., pull: bool = ...) -> None: ...

class CacheInfo(_message.Message):
    __slots__ = ("uri", "status", "in_cache", "timestamp", "name", "storage", "last_modified", "saved_version", "debug_metadata", "cache_id", "last_hit", "hits", "pinned")
    class DebugMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    URI_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IN_CACHE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    SAVED_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEBUG_METADATA_FIELD_NUMBER: _ClassVar[int]
    CACHE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_HIT_FIELD_NUMBER: _ClassVar[int]
    HITS_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    uri: str
    status: str
    in_cache: bool
    timestamp: int
    name: str
    storage: str
    last_modified: str
    saved_version: str
    debug_metadata: _containers.ScalarMap[str, int]
    cache_id: str
    last_hit: int
    hits: int
    pinned: bool
    def __init__(self, uri: _Optional[str] = ..., status: _Optional[str] = ..., in_cache: bool = ..., timestamp: _Optional[int] = ..., name: _Optional[str] = ..., storage: _Optional[str] = ..., last_modified: _Optional[str] = ..., saved_version: _Optional[str] = ..., debug_metadata: _Optional[_Mapping[str, int]] = ..., cache_id: _Optional[str] = ..., last_hit: _Optional[int] = ..., hits: _Optional[int] = ..., pinned: bool = ...) -> None: ...

class DropRequest(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class ListRequest(_message.Message):
    __slots__ = ("status_filter",)
    STATUS_FILTER_FIELD_NUMBER: _ClassVar[int]
    status_filter: str
    def __init__(self, status_filter: _Optional[str] = ...) -> None: ...

class ProjectRequest(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class ProjectInfo(_message.Message):
    __slots__ = ("status", "uri", "filename", "crs", "last_modified", "storage", "has_bad_layers", "layers", "cache_id")
    class Layer(_message.Message):
        __slots__ = ("layer_id", "name", "source", "crs", "is_valid", "is_spatial")
        LAYER_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        CRS_FIELD_NUMBER: _ClassVar[int]
        IS_VALID_FIELD_NUMBER: _ClassVar[int]
        IS_SPATIAL_FIELD_NUMBER: _ClassVar[int]
        layer_id: str
        name: str
        source: str
        crs: str
        is_valid: bool
        is_spatial: bool
        def __init__(self, layer_id: _Optional[str] = ..., name: _Optional[str] = ..., source: _Optional[str] = ..., crs: _Optional[str] = ..., is_valid: bool = ..., is_spatial: bool = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CRS_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    HAS_BAD_LAYERS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    CACHE_ID_FIELD_NUMBER: _ClassVar[int]
    status: str
    uri: str
    filename: str
    crs: str
    last_modified: str
    storage: str
    has_bad_layers: bool
    layers: _containers.RepeatedCompositeFieldContainer[ProjectInfo.Layer]
    cache_id: str
    def __init__(self, status: _Optional[str] = ..., uri: _Optional[str] = ..., filename: _Optional[str] = ..., crs: _Optional[str] = ..., last_modified: _Optional[str] = ..., storage: _Optional[str] = ..., has_bad_layers: bool = ..., layers: _Optional[_Iterable[_Union[ProjectInfo.Layer, _Mapping]]] = ..., cache_id: _Optional[str] = ...) -> None: ...

class PluginInfo(_message.Message):
    __slots__ = ("name", "path", "plugin_type", "metadata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    path: str
    plugin_type: str
    metadata: str
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., plugin_type: _Optional[str] = ..., metadata: _Optional[str] = ...) -> None: ...

class JsonConfig(_message.Message):
    __slots__ = ("json",)
    JSON_FIELD_NUMBER: _ClassVar[int]
    json: str
    def __init__(self, json: _Optional[str] = ...) -> None: ...

class CatalogRequest(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: str
    def __init__(self, location: _Optional[str] = ...) -> None: ...

class CatalogItem(_message.Message):
    __slots__ = ("uri", "name", "storage", "last_modified", "public_uri")
    URI_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    name: str
    storage: str
    last_modified: str
    public_uri: str
    def __init__(self, uri: _Optional[str] = ..., name: _Optional[str] = ..., storage: _Optional[str] = ..., last_modified: _Optional[str] = ..., public_uri: _Optional[str] = ...) -> None: ...