# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tapi.proto\x12\x03\x61pi\"\x1b\n\x0bPingRequest\x12\x0c\n\x04\x65\x63ho\x18\x01 \x01(\t\"\x19\n\tPingReply\x12\x0c\n\x04\x65\x63ho\x18\x01 \x01(\t\"\x07\n\x05\x45mpty\"\x1e\n\rResponseChunk\x12\r\n\x05\x63hunk\x18\x01 \x01(\x0c\"\xe4\x01\n\nOwsRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\x12\x0f\n\x07request\x18\x02 \x01(\t\x12\x0e\n\x06target\x18\x03 \x01(\t\x12\x14\n\x07version\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x03url\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x13\n\x06\x64irect\x18\x06 \x01(\x08H\x02\x88\x01\x01\x12\x14\n\x07options\x18\x07 \x01(\tH\x03\x88\x01\x01\x12\x17\n\nrequest_id\x18\x08 \x01(\tH\x04\x88\x01\x01\x42\n\n\x08_versionB\x06\n\x04_urlB\t\n\x07_directB\n\n\x08_optionsB\r\n\x0b_request_id\"\xd3\x01\n\x0eGenericRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\x11\n\x04\x64\x61ta\x18\x03 \x01(\x0cH\x00\x88\x01\x01\x12\x13\n\x06target\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07version\x18\x05 \x01(\tH\x02\x88\x01\x01\x12\x13\n\x06\x64irect\x18\x06 \x01(\x08H\x03\x88\x01\x01\x12\x17\n\nrequest_id\x18\x07 \x01(\tH\x04\x88\x01\x01\x42\x07\n\x05_dataB\t\n\x07_targetB\n\n\x08_versionB\t\n\x07_directB\r\n\x0b_request_id\":\n\x0f\x43heckoutRequest\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x11\n\x04pull\x18\x02 \x01(\x08H\x00\x88\x01\x01\x42\x07\n\x05_pull\"\xc5\x02\n\tCacheInfo\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x10\n\x08in_cache\x18\x03 \x01(\x08\x12\x11\n\x04name\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07storage\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x1a\n\rlast_modified\x18\x06 \x01(\tH\x02\x88\x01\x01\x12\x1a\n\rsaved_version\x18\x07 \x01(\tH\x03\x88\x01\x01\x12\x39\n\x0e\x64\x65\x62ug_metadata\x18\x08 \x03(\x0b\x32!.api.CacheInfo.DebugMetadataEntry\x1a\x34\n\x12\x44\x65\x62ugMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\x42\x07\n\x05_nameB\n\n\x08_storageB\x10\n\x0e_last_modifiedB\x10\n\x0e_saved_version\"\x1a\n\x0b\x44ropRequest\x12\x0b\n\x03uri\x18\x01 \x01(\t\";\n\x0bListRequest\x12\x1a\n\rstatus_filter\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x10\n\x0e_status_filter\"T\n\nPluginInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x13\n\x0bplugin_type\x18\x03 \x01(\t\x12\x15\n\rjson_metadata\x18\x04 \x01(\t2\xae\x03\n\nQgisWorker\x12*\n\x04Ping\x12\x10.api.PingRequest\x1a\x0e.api.PingReply\"\x00\x12<\n\x11\x45xecuteOwsRequest\x12\x0f.api.OwsRequest\x1a\x12.api.ResponseChunk\"\x00\x30\x01\x12=\n\x0e\x45xecuteRequest\x12\x13.api.GenericRequest\x1a\x12.api.ResponseChunk\"\x00\x30\x01\x12\x39\n\x0f\x43heckoutProject\x12\x14.api.CheckoutRequest\x1a\x0e.api.CacheInfo\"\x00\x12\x31\n\x0b\x44ropProject\x12\x10.api.DropRequest\x1a\x0e.api.CacheInfo\"\x00\x12&\n\nClearCache\x12\n.api.Empty\x1a\n.api.Empty\"\x00\x12\x31\n\tListCache\x12\x10.api.ListRequest\x1a\x0e.api.CacheInfo\"\x00\x30\x01\x12.\n\x0bListPlugins\x12\n.api.Empty\x1a\x0f.api.PluginInfo\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CACHEINFO_DEBUGMETADATAENTRY._options = None
  _CACHEINFO_DEBUGMETADATAENTRY._serialized_options = b'8\001'
  _globals['_PINGREQUEST']._serialized_start=18
  _globals['_PINGREQUEST']._serialized_end=45
  _globals['_PINGREPLY']._serialized_start=47
  _globals['_PINGREPLY']._serialized_end=72
  _globals['_EMPTY']._serialized_start=74
  _globals['_EMPTY']._serialized_end=81
  _globals['_RESPONSECHUNK']._serialized_start=83
  _globals['_RESPONSECHUNK']._serialized_end=113
  _globals['_OWSREQUEST']._serialized_start=116
  _globals['_OWSREQUEST']._serialized_end=344
  _globals['_GENERICREQUEST']._serialized_start=347
  _globals['_GENERICREQUEST']._serialized_end=558
  _globals['_CHECKOUTREQUEST']._serialized_start=560
  _globals['_CHECKOUTREQUEST']._serialized_end=618
  _globals['_CACHEINFO']._serialized_start=621
  _globals['_CACHEINFO']._serialized_end=946
  _globals['_CACHEINFO_DEBUGMETADATAENTRY']._serialized_start=837
  _globals['_CACHEINFO_DEBUGMETADATAENTRY']._serialized_end=889
  _globals['_DROPREQUEST']._serialized_start=948
  _globals['_DROPREQUEST']._serialized_end=974
  _globals['_LISTREQUEST']._serialized_start=976
  _globals['_LISTREQUEST']._serialized_end=1035
  _globals['_PLUGININFO']._serialized_start=1037
  _globals['_PLUGININFO']._serialized_end=1121
  _globals['_QGISWORKER']._serialized_start=1124
  _globals['_QGISWORKER']._serialized_end=1554
# @@protoc_insertion_point(module_scope)