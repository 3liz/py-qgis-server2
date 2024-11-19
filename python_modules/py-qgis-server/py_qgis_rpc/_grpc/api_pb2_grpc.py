# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import api_pb2 as api__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in api_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class QgisServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
                '/api.QgisServer/Ping',
                request_serializer=api__pb2.PingRequest.SerializeToString,
                response_deserializer=api__pb2.PingReply.FromString,
                _registered_method=True)
        self.ExecuteOwsRequest = channel.unary_stream(
                '/api.QgisServer/ExecuteOwsRequest',
                request_serializer=api__pb2.OwsRequest.SerializeToString,
                response_deserializer=api__pb2.ResponseChunk.FromString,
                _registered_method=True)
        self.ExecuteApiRequest = channel.unary_stream(
                '/api.QgisServer/ExecuteApiRequest',
                request_serializer=api__pb2.ApiRequest.SerializeToString,
                response_deserializer=api__pb2.ResponseChunk.FromString,
                _registered_method=True)
        self.ExecuteRequest = channel.unary_stream(
                '/api.QgisServer/ExecuteRequest',
                request_serializer=api__pb2.GenericRequest.SerializeToString,
                response_deserializer=api__pb2.ResponseChunk.FromString,
                _registered_method=True)


class QgisServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExecuteOwsRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExecuteApiRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExecuteRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QgisServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=api__pb2.PingRequest.FromString,
                    response_serializer=api__pb2.PingReply.SerializeToString,
            ),
            'ExecuteOwsRequest': grpc.unary_stream_rpc_method_handler(
                    servicer.ExecuteOwsRequest,
                    request_deserializer=api__pb2.OwsRequest.FromString,
                    response_serializer=api__pb2.ResponseChunk.SerializeToString,
            ),
            'ExecuteApiRequest': grpc.unary_stream_rpc_method_handler(
                    servicer.ExecuteApiRequest,
                    request_deserializer=api__pb2.ApiRequest.FromString,
                    response_serializer=api__pb2.ResponseChunk.SerializeToString,
            ),
            'ExecuteRequest': grpc.unary_stream_rpc_method_handler(
                    servicer.ExecuteRequest,
                    request_deserializer=api__pb2.GenericRequest.FromString,
                    response_serializer=api__pb2.ResponseChunk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'api.QgisServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('api.QgisServer', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class QgisServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisServer/Ping',
            api__pb2.PingRequest.SerializeToString,
            api__pb2.PingReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ExecuteOwsRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisServer/ExecuteOwsRequest',
            api__pb2.OwsRequest.SerializeToString,
            api__pb2.ResponseChunk.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ExecuteApiRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisServer/ExecuteApiRequest',
            api__pb2.ApiRequest.SerializeToString,
            api__pb2.ResponseChunk.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ExecuteRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisServer/ExecuteRequest',
            api__pb2.GenericRequest.SerializeToString,
            api__pb2.ResponseChunk.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class QgisAdminStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
                '/api.QgisAdmin/Ping',
                request_serializer=api__pb2.PingRequest.SerializeToString,
                response_deserializer=api__pb2.PingReply.FromString,
                _registered_method=True)
        self.CheckoutProject = channel.unary_stream(
                '/api.QgisAdmin/CheckoutProject',
                request_serializer=api__pb2.CheckoutRequest.SerializeToString,
                response_deserializer=api__pb2.CacheInfo.FromString,
                _registered_method=True)
        self.PullProjects = channel.stream_stream(
                '/api.QgisAdmin/PullProjects',
                request_serializer=api__pb2.ProjectRequest.SerializeToString,
                response_deserializer=api__pb2.CacheInfo.FromString,
                _registered_method=True)
        self.DropProject = channel.unary_stream(
                '/api.QgisAdmin/DropProject',
                request_serializer=api__pb2.DropRequest.SerializeToString,
                response_deserializer=api__pb2.CacheInfo.FromString,
                _registered_method=True)
        self.ListCache = channel.unary_stream(
                '/api.QgisAdmin/ListCache',
                request_serializer=api__pb2.ListRequest.SerializeToString,
                response_deserializer=api__pb2.CacheInfo.FromString,
                _registered_method=True)
        self.ClearCache = channel.unary_unary(
                '/api.QgisAdmin/ClearCache',
                request_serializer=api__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.Empty.FromString,
                _registered_method=True)
        self.UpdateCache = channel.unary_stream(
                '/api.QgisAdmin/UpdateCache',
                request_serializer=api__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.CacheInfo.FromString,
                _registered_method=True)
        self.ListPlugins = channel.unary_stream(
                '/api.QgisAdmin/ListPlugins',
                request_serializer=api__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.PluginInfo.FromString,
                _registered_method=True)
        self.SetConfig = channel.unary_unary(
                '/api.QgisAdmin/SetConfig',
                request_serializer=api__pb2.JsonConfig.SerializeToString,
                response_deserializer=api__pb2.Empty.FromString,
                _registered_method=True)
        self.GetConfig = channel.unary_unary(
                '/api.QgisAdmin/GetConfig',
                request_serializer=api__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.JsonConfig.FromString,
                _registered_method=True)
        self.ReloadConfig = channel.unary_unary(
                '/api.QgisAdmin/ReloadConfig',
                request_serializer=api__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.Empty.FromString,
                _registered_method=True)
        self.GetProjectInfo = channel.unary_unary(
                '/api.QgisAdmin/GetProjectInfo',
                request_serializer=api__pb2.ProjectRequest.SerializeToString,
                response_deserializer=api__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.Catalog = channel.unary_stream(
                '/api.QgisAdmin/Catalog',
                request_serializer=api__pb2.CatalogRequest.SerializeToString,
                response_deserializer=api__pb2.CatalogItem.FromString,
                _registered_method=True)
        self.GetEnv = channel.unary_unary(
                '/api.QgisAdmin/GetEnv',
                request_serializer=api__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.JsonConfig.FromString,
                _registered_method=True)
        self.SetServerServingStatus = channel.unary_unary(
                '/api.QgisAdmin/SetServerServingStatus',
                request_serializer=api__pb2.ServerStatus.SerializeToString,
                response_deserializer=api__pb2.Empty.FromString,
                _registered_method=True)
        self.Stats = channel.unary_unary(
                '/api.QgisAdmin/Stats',
                request_serializer=api__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.StatsReply.FromString,
                _registered_method=True)
        self.Test = channel.unary_unary(
                '/api.QgisAdmin/Test',
                request_serializer=api__pb2.TestRequest.SerializeToString,
                response_deserializer=api__pb2.Empty.FromString,
                _registered_method=True)


class QgisAdminServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckoutProject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PullProjects(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DropProject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCache(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearCache(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateCache(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListPlugins(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReloadConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProjectInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Catalog(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEnv(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetServerServingStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Test(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QgisAdminServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=api__pb2.PingRequest.FromString,
                    response_serializer=api__pb2.PingReply.SerializeToString,
            ),
            'CheckoutProject': grpc.unary_stream_rpc_method_handler(
                    servicer.CheckoutProject,
                    request_deserializer=api__pb2.CheckoutRequest.FromString,
                    response_serializer=api__pb2.CacheInfo.SerializeToString,
            ),
            'PullProjects': grpc.stream_stream_rpc_method_handler(
                    servicer.PullProjects,
                    request_deserializer=api__pb2.ProjectRequest.FromString,
                    response_serializer=api__pb2.CacheInfo.SerializeToString,
            ),
            'DropProject': grpc.unary_stream_rpc_method_handler(
                    servicer.DropProject,
                    request_deserializer=api__pb2.DropRequest.FromString,
                    response_serializer=api__pb2.CacheInfo.SerializeToString,
            ),
            'ListCache': grpc.unary_stream_rpc_method_handler(
                    servicer.ListCache,
                    request_deserializer=api__pb2.ListRequest.FromString,
                    response_serializer=api__pb2.CacheInfo.SerializeToString,
            ),
            'ClearCache': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearCache,
                    request_deserializer=api__pb2.Empty.FromString,
                    response_serializer=api__pb2.Empty.SerializeToString,
            ),
            'UpdateCache': grpc.unary_stream_rpc_method_handler(
                    servicer.UpdateCache,
                    request_deserializer=api__pb2.Empty.FromString,
                    response_serializer=api__pb2.CacheInfo.SerializeToString,
            ),
            'ListPlugins': grpc.unary_stream_rpc_method_handler(
                    servicer.ListPlugins,
                    request_deserializer=api__pb2.Empty.FromString,
                    response_serializer=api__pb2.PluginInfo.SerializeToString,
            ),
            'SetConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.SetConfig,
                    request_deserializer=api__pb2.JsonConfig.FromString,
                    response_serializer=api__pb2.Empty.SerializeToString,
            ),
            'GetConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConfig,
                    request_deserializer=api__pb2.Empty.FromString,
                    response_serializer=api__pb2.JsonConfig.SerializeToString,
            ),
            'ReloadConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.ReloadConfig,
                    request_deserializer=api__pb2.Empty.FromString,
                    response_serializer=api__pb2.Empty.SerializeToString,
            ),
            'GetProjectInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProjectInfo,
                    request_deserializer=api__pb2.ProjectRequest.FromString,
                    response_serializer=api__pb2.ProjectInfo.SerializeToString,
            ),
            'Catalog': grpc.unary_stream_rpc_method_handler(
                    servicer.Catalog,
                    request_deserializer=api__pb2.CatalogRequest.FromString,
                    response_serializer=api__pb2.CatalogItem.SerializeToString,
            ),
            'GetEnv': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEnv,
                    request_deserializer=api__pb2.Empty.FromString,
                    response_serializer=api__pb2.JsonConfig.SerializeToString,
            ),
            'SetServerServingStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.SetServerServingStatus,
                    request_deserializer=api__pb2.ServerStatus.FromString,
                    response_serializer=api__pb2.Empty.SerializeToString,
            ),
            'Stats': grpc.unary_unary_rpc_method_handler(
                    servicer.Stats,
                    request_deserializer=api__pb2.Empty.FromString,
                    response_serializer=api__pb2.StatsReply.SerializeToString,
            ),
            'Test': grpc.unary_unary_rpc_method_handler(
                    servicer.Test,
                    request_deserializer=api__pb2.TestRequest.FromString,
                    response_serializer=api__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'api.QgisAdmin', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('api.QgisAdmin', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class QgisAdmin(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/Ping',
            api__pb2.PingRequest.SerializeToString,
            api__pb2.PingReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CheckoutProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisAdmin/CheckoutProject',
            api__pb2.CheckoutRequest.SerializeToString,
            api__pb2.CacheInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PullProjects(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/api.QgisAdmin/PullProjects',
            api__pb2.ProjectRequest.SerializeToString,
            api__pb2.CacheInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DropProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisAdmin/DropProject',
            api__pb2.DropRequest.SerializeToString,
            api__pb2.CacheInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListCache(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisAdmin/ListCache',
            api__pb2.ListRequest.SerializeToString,
            api__pb2.CacheInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ClearCache(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/ClearCache',
            api__pb2.Empty.SerializeToString,
            api__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateCache(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisAdmin/UpdateCache',
            api__pb2.Empty.SerializeToString,
            api__pb2.CacheInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListPlugins(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisAdmin/ListPlugins',
            api__pb2.Empty.SerializeToString,
            api__pb2.PluginInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/SetConfig',
            api__pb2.JsonConfig.SerializeToString,
            api__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/GetConfig',
            api__pb2.Empty.SerializeToString,
            api__pb2.JsonConfig.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReloadConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/ReloadConfig',
            api__pb2.Empty.SerializeToString,
            api__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetProjectInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/GetProjectInfo',
            api__pb2.ProjectRequest.SerializeToString,
            api__pb2.ProjectInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Catalog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/api.QgisAdmin/Catalog',
            api__pb2.CatalogRequest.SerializeToString,
            api__pb2.CatalogItem.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetEnv(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/GetEnv',
            api__pb2.Empty.SerializeToString,
            api__pb2.JsonConfig.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetServerServingStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/SetServerServingStatus',
            api__pb2.ServerStatus.SerializeToString,
            api__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Stats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/Stats',
            api__pb2.Empty.SerializeToString,
            api__pb2.StatsReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Test(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/api.QgisAdmin/Test',
            api__pb2.TestRequest.SerializeToString,
            api__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
