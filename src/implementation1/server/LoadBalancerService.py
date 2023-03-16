from datetime import datetime
from google.protobuf import timestamp_pb2 as _timestamp_pb2


class LoadBalancerService:
    def send_meteo_data(self, temperature, humidity, timestamp):
        print(f'Data recived: tmp={str(temperature)} hum={str(humidity)} timestamp={str(timestamp)}')
        return 'Done'

    def send_pollution_data(self, co2, timestamp):
        print(f'Data recived: co2={str(co2)} timestamp={str(timestamp)}')
        return 'Done'


lb_service = LoadBalancerService()
