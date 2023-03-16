from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RawMeteoData(_message.Message):
    __slots__ = ["humidity", "temperature"]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    humidity: float
    temperature: float
    def __init__(self, temperature: _Optional[float] = ..., humidity: _Optional[float] = ...) -> None: ...

class RawPollutionData(_message.Message):
    __slots__ = ["co2"]
    CO2_FIELD_NUMBER: _ClassVar[int]
    co2: float
    def __init__(self, co2: _Optional[float] = ...) -> None: ...
