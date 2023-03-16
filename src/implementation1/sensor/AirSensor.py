import src.implementation1.gRPC.MeteoServer_pb2 as MeteoServer__pb2
from src.implementation1.sensor.Sensor import Sensor
from google.protobuf import timestamp_pb2 as _timestamp_pb2

class AirSensor(Sensor):
    def __init__(self):
        super().__init__()

    def _data_measured(self):
        ts = _timestamp_pb2.Timestamp()
        ts.GetCurrentTime()
        return MeteoServer__pb2.RawMeteoData(
            temperature=self._sensor.gen_temperature(),
            humidity=self._sensor.gen_humidity(),
            timestamp=ts
        )

    def _grpc_function_name(self) -> str:
        return "SendMeteoData"


AirSensor()
