# import datetime
# from google.protobuf.timestamp_pb2 import Timestamp
import src.implementation1.gRPC.MeteoServer_pb2 as MeteoServer__pb2
from src.implementation1.sensor.Sensor import Sensor


class AirSensor(Sensor):
    def __init__(self):
        super().__init__()

    def _data_measured(self):
        # now = datetime.datetime.now()
        # print(type(self._sensor.gen_humidity()))
        return MeteoServer__pb2.RawMeteoData(
            temperature=self._sensor.gen_temperature(),
            humidity=self._sensor.gen_humidity()
        )

    def _grpc_function_name(self) -> str:
        return "SendMeteoData"


AirSensor()
