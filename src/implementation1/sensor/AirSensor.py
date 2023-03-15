import datetime

from src.implementation1.sensor.Sensor import Sensor
import grpc

import src.implementation1.gRPC.MeteoServer_pb2 as MeteoServer__pb2
import src.implementation1.gRPC.MeteoServer_pb2_grpc as MeteoServer__pb2_grpc

class AirSensor(Sensor):
    def _send_data(self):
        date = datetime.datetime.now()
        print(type(self._sensor.gen_humidity()))
        raw_meteo_data = MeteoServer__pb2.RawMeteoData(temperature=self._sensor.gen_temperature(),humidity=self._sensor.gen_humidity())
        print(raw_meteo_data)
        stub.SendMeteoData(raw_meteo_data)



#open gRPC channel
channel = grpc.insecure_channel('localhost:50051')

#create a stub (client)
stub = MeteoServer__pb2_grpc.LoadBalancerServiceStub(channel)

#create a valid request
airS = AirSensor()
airS._send_data()
