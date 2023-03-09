import time

from src.implementation1.meteo_utils import MeteoDataDetector
from src.implementation1.sensor.RawMeteoData import RawMeteoData
from src.implementation1.sensor.Sensor import Sensor
import grpc

from src.implementation1.gRPC import MeteoServer_pb2
from src.implementation1.gRPC import MeteoServer_pb2_grpc




class AirSensor(Sensor):
    def _send_data(self):
        rawMeteoData = MeteoServer_pb2.RawMeteoData(temperature=self._detector.gen_temperature(),humidity=self.gen_temperature(),timestamp=time.time())
        stub.SendMeteoData(rawMeteoData)



#open gRPC channel
channel = grpc.insecure_channel('localhost:50051')

#create a stub (client)
stub = MeteoServer_pb2_grpc.LoadBalancerServiceStub(channel)

#create a valid request
airS = AirSensor()
airS._send_data()
