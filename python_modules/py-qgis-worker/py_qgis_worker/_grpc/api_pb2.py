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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tapi.proto\x12\x03\x61pi\"\x1b\n\x0bPingRequest\x12\x0c\n\x04\x65\x63ho\x18\x01 \x01(\t\"\x19\n\tPingReply\x12\x0c\n\x04\x65\x63ho\x18\x01 \x01(\t\"\x07\n\x05\x45mpty\"\x85\x01\n\nStatsReply\x12\x13\n\x0bnum_workers\x18\x02 \x01(\x05\x12\x17\n\x0fstopped_workers\x18\x03 \x01(\x05\x12\x1f\n\x17worker_failure_pressure\x18\x04 \x01(\x02\x12\x18\n\x10request_pressure\x18\x05 \x01(\x02\x12\x0e\n\x06uptime\x18\x06 \x01(\x05\"2\n\x0cServerStatus\x12\"\n\x06status\x18\x01 \x01(\x0e\x32\x12.api.ServingStatus\"\x1e\n\rResponseChunk\x12\r\n\x05\x63hunk\x18\x01 \x01(\x0c\"\x90\x02\n\nOwsRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\x12\x0f\n\x07request\x18\x02 \x01(\t\x12\x0e\n\x06target\x18\x03 \x01(\t\x12\x14\n\x07version\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x03url\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x13\n\x06\x64irect\x18\x06 \x01(\x08H\x02\x88\x01\x01\x12\x14\n\x07options\x18\x07 \x01(\tH\x03\x88\x01\x01\x12\x17\n\nrequest_id\x18\x08 \x01(\tH\x04\x88\x01\x01\x12\x19\n\x0c\x64\x65\x62ug_report\x18\t \x01(\x08H\x05\x88\x01\x01\x42\n\n\x08_versionB\x06\n\x04_urlB\t\n\x07_directB\n\n\x08_optionsB\r\n\x0b_request_idB\x0f\n\r_debug_report\"\xa4\x02\n\nApiRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0e\n\x06method\x18\x03 \x01(\t\x12\x11\n\x04\x64\x61ta\x18\x04 \x01(\x0cH\x00\x88\x01\x01\x12\x13\n\x06target\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x10\n\x03url\x18\x06 \x01(\tH\x02\x88\x01\x01\x12\x13\n\x06\x64irect\x18\x07 \x01(\x08H\x03\x88\x01\x01\x12\x14\n\x07options\x18\x08 \x01(\tH\x04\x88\x01\x01\x12\x17\n\nrequest_id\x18\t \x01(\tH\x05\x88\x01\x01\x12\x19\n\x0c\x64\x65\x62ug_report\x18\n \x01(\x08H\x06\x88\x01\x01\x42\x07\n\x05_dataB\t\n\x07_targetB\x06\n\x04_urlB\t\n\x07_directB\n\n\x08_optionsB\r\n\x0b_request_idB\x0f\n\r_debug_report\"\xdd\x01\n\x0eGenericRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\x11\n\x04\x64\x61ta\x18\x03 \x01(\x0cH\x00\x88\x01\x01\x12\x13\n\x06target\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x13\n\x06\x64irect\x18\x06 \x01(\x08H\x02\x88\x01\x01\x12\x17\n\nrequest_id\x18\x07 \x01(\tH\x03\x88\x01\x01\x12\x19\n\x0c\x64\x65\x62ug_report\x18\t \x01(\x08H\x04\x88\x01\x01\x42\x07\n\x05_dataB\t\n\x07_targetB\t\n\x07_directB\r\n\x0b_request_idB\x0f\n\r_debug_report\":\n\x0f\x43heckoutRequest\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x11\n\x04pull\x18\x02 \x01(\x08H\x00\x88\x01\x01\x42\x07\n\x05_pull\"\xfc\x02\n\tCacheInfo\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x10\n\x08in_cache\x18\x03 \x01(\x08\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\x12\x11\n\x04name\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07storage\x18\x06 \x01(\tH\x01\x88\x01\x01\x12\x1a\n\rlast_modified\x18\x07 \x01(\tH\x02\x88\x01\x01\x12\x1a\n\rsaved_version\x18\x08 \x01(\tH\x03\x88\x01\x01\x12\x39\n\x0e\x64\x65\x62ug_metadata\x18\t \x03(\x0b\x32!.api.CacheInfo.DebugMetadataEntry\x12\x15\n\x08\x63\x61\x63he_id\x18\n \x01(\tH\x04\x88\x01\x01\x1a\x34\n\x12\x44\x65\x62ugMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\x42\x07\n\x05_nameB\n\n\x08_storageB\x10\n\x0e_last_modifiedB\x10\n\x0e_saved_versionB\x0b\n\t_cache_id\"\x1a\n\x0b\x44ropRequest\x12\x0b\n\x03uri\x18\x01 \x01(\t\";\n\x0bListRequest\x12\x1a\n\rstatus_filter\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x10\n\x0e_status_filter\"\x1d\n\x0eProjectRequest\x12\x0b\n\x03uri\x18\x01 \x01(\t\"\xc1\x02\n\x0bProjectInfo\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0b\n\x03uri\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\x12\x0b\n\x03\x63rs\x18\x04 \x01(\t\x12\x15\n\rlast_modified\x18\x05 \x01(\t\x12\x0f\n\x07storage\x18\x06 \x01(\t\x12\x16\n\x0ehas_bad_layers\x18\x07 \x01(\x08\x12&\n\x06layers\x18\x08 \x03(\x0b\x32\x16.api.ProjectInfo.Layer\x12\x15\n\x08\x63\x61\x63he_id\x18\t \x01(\tH\x00\x88\x01\x01\x1aj\n\x05Layer\x12\x10\n\x08layer_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06source\x18\x03 \x01(\t\x12\x0b\n\x03\x63rs\x18\x04 \x01(\t\x12\x10\n\x08is_valid\x18\x05 \x01(\x08\x12\x12\n\nis_spatial\x18\x06 \x01(\x08\x42\x0b\n\t_cache_id\"O\n\nPluginInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x13\n\x0bplugin_type\x18\x03 \x01(\t\x12\x10\n\x08metadata\x18\x04 \x01(\t\"\x1a\n\nJsonConfig\x12\x0c\n\x04json\x18\x01 \x01(\t\"4\n\x0e\x43\x61talogRequest\x12\x15\n\x08location\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_location\"d\n\x0b\x43\x61talogItem\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07storage\x18\x03 \x01(\t\x12\x15\n\rlast_modified\x18\x04 \x01(\t\x12\x12\n\npublic_uri\x18\x05 \x01(\t*-\n\rServingStatus\x12\x0b\n\x07SERVING\x10\x00\x12\x0f\n\x0bNOT_SERVING\x10\x01\x32\xf3\x01\n\nQgisServer\x12*\n\x04Ping\x12\x10.api.PingRequest\x1a\x0e.api.PingReply\"\x00\x12<\n\x11\x45xecuteOwsRequest\x12\x0f.api.OwsRequest\x1a\x12.api.ResponseChunk\"\x00\x30\x01\x12<\n\x11\x45xecuteApiRequest\x12\x0f.api.ApiRequest\x1a\x12.api.ResponseChunk\"\x00\x30\x01\x12=\n\x0e\x45xecuteRequest\x12\x13.api.GenericRequest\x1a\x12.api.ResponseChunk\"\x00\x30\x01\x32\x9d\x06\n\tQgisAdmin\x12*\n\x04Ping\x12\x10.api.PingRequest\x1a\x0e.api.PingReply\"\x00\x12;\n\x0f\x43heckoutProject\x12\x14.api.CheckoutRequest\x1a\x0e.api.CacheInfo\"\x00\x30\x01\x12\x39\n\x0cPullProjects\x12\x13.api.ProjectRequest\x1a\x0e.api.CacheInfo\"\x00(\x01\x30\x01\x12\x33\n\x0b\x44ropProject\x12\x10.api.DropRequest\x1a\x0e.api.CacheInfo\"\x00\x30\x01\x12\x31\n\tListCache\x12\x10.api.ListRequest\x1a\x0e.api.CacheInfo\"\x00\x30\x01\x12&\n\nClearCache\x12\n.api.Empty\x1a\n.api.Empty\"\x00\x12-\n\x0bUpdateCache\x12\n.api.Empty\x1a\x0e.api.CacheInfo\"\x00\x30\x01\x12.\n\x0bListPlugins\x12\n.api.Empty\x1a\x0f.api.PluginInfo\"\x00\x30\x01\x12*\n\tSetConfig\x12\x0f.api.JsonConfig\x1a\n.api.Empty\"\x00\x12*\n\tGetConfig\x12\n.api.Empty\x1a\x0f.api.JsonConfig\"\x00\x12(\n\x0cReloadConfig\x12\n.api.Empty\x1a\n.api.Empty\"\x00\x12\x39\n\x0eGetProjectInfo\x12\x13.api.ProjectRequest\x1a\x10.api.ProjectInfo\"\x00\x12\x34\n\x07\x43\x61talog\x12\x13.api.CatalogRequest\x1a\x10.api.CatalogItem\"\x00\x30\x01\x12\'\n\x06GetEnv\x12\n.api.Empty\x1a\x0f.api.JsonConfig\"\x00\x12\x39\n\x16SetServerServingStatus\x12\x11.api.ServerStatus\x1a\n.api.Empty\"\x00\x12&\n\x05Stats\x12\n.api.Empty\x1a\x0f.api.StatsReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CACHEINFO_DEBUGMETADATAENTRY._options = None
  _CACHEINFO_DEBUGMETADATAENTRY._serialized_options = b'8\001'
  _globals['_SERVINGSTATUS']._serialized_start=2249
  _globals['_SERVINGSTATUS']._serialized_end=2294
  _globals['_PINGREQUEST']._serialized_start=18
  _globals['_PINGREQUEST']._serialized_end=45
  _globals['_PINGREPLY']._serialized_start=47
  _globals['_PINGREPLY']._serialized_end=72
  _globals['_EMPTY']._serialized_start=74
  _globals['_EMPTY']._serialized_end=81
  _globals['_STATSREPLY']._serialized_start=84
  _globals['_STATSREPLY']._serialized_end=217
  _globals['_SERVERSTATUS']._serialized_start=219
  _globals['_SERVERSTATUS']._serialized_end=269
  _globals['_RESPONSECHUNK']._serialized_start=271
  _globals['_RESPONSECHUNK']._serialized_end=301
  _globals['_OWSREQUEST']._serialized_start=304
  _globals['_OWSREQUEST']._serialized_end=576
  _globals['_APIREQUEST']._serialized_start=579
  _globals['_APIREQUEST']._serialized_end=871
  _globals['_GENERICREQUEST']._serialized_start=874
  _globals['_GENERICREQUEST']._serialized_end=1095
  _globals['_CHECKOUTREQUEST']._serialized_start=1097
  _globals['_CHECKOUTREQUEST']._serialized_end=1155
  _globals['_CACHEINFO']._serialized_start=1158
  _globals['_CACHEINFO']._serialized_end=1538
  _globals['_CACHEINFO_DEBUGMETADATAENTRY']._serialized_start=1416
  _globals['_CACHEINFO_DEBUGMETADATAENTRY']._serialized_end=1468
  _globals['_DROPREQUEST']._serialized_start=1540
  _globals['_DROPREQUEST']._serialized_end=1566
  _globals['_LISTREQUEST']._serialized_start=1568
  _globals['_LISTREQUEST']._serialized_end=1627
  _globals['_PROJECTREQUEST']._serialized_start=1629
  _globals['_PROJECTREQUEST']._serialized_end=1658
  _globals['_PROJECTINFO']._serialized_start=1661
  _globals['_PROJECTINFO']._serialized_end=1982
  _globals['_PROJECTINFO_LAYER']._serialized_start=1863
  _globals['_PROJECTINFO_LAYER']._serialized_end=1969
  _globals['_PLUGININFO']._serialized_start=1984
  _globals['_PLUGININFO']._serialized_end=2063
  _globals['_JSONCONFIG']._serialized_start=2065
  _globals['_JSONCONFIG']._serialized_end=2091
  _globals['_CATALOGREQUEST']._serialized_start=2093
  _globals['_CATALOGREQUEST']._serialized_end=2145
  _globals['_CATALOGITEM']._serialized_start=2147
  _globals['_CATALOGITEM']._serialized_end=2247
  _globals['_QGISSERVER']._serialized_start=2297
  _globals['_QGISSERVER']._serialized_end=2540
  _globals['_QGISADMIN']._serialized_start=2543
  _globals['_QGISADMIN']._serialized_end=3340
# @@protoc_insertion_point(module_scope)
