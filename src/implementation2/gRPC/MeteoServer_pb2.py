# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/implementation1/gRPC/MeteoServer.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*src/implementation1/gRPC/MeteoServer.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"d\n\x0cRawMeteoData\x12\x13\n\x0btemperature\x18\x01 \x01(\x02\x12\x10\n\x08humidity\x18\x02 \x01(\x02\x12-\n\ttimestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"N\n\x10RawPollutionData\x12\x0b\n\x03\x63o2\x18\x01 \x01(\x02\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2\x91\x01\n\x13LoadBalancerService\x12\x38\n\rSendMeteoData\x12\r.RawMeteoData\x1a\x16.google.protobuf.Empty\"\x00\x12@\n\x11SendPollutionData\x12\x11.RawPollutionData\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'src.implementation1.gRPC.MeteoServer_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RAWMETEODATA._serialized_start=108
  _RAWMETEODATA._serialized_end=208
  _RAWPOLLUTIONDATA._serialized_start=210
  _RAWPOLLUTIONDATA._serialized_end=288
  _LOADBALANCERSERVICE._serialized_start=291
  _LOADBALANCERSERVICE._serialized_end=436
# @@protoc_insertion_point(module_scope)
