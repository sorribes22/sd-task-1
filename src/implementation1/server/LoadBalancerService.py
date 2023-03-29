import os
from datetime import datetime

import grpc
from dotenv import load_dotenv
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import src.implementation1.gRPC.DataProcessor_pb2 as DataProcessor__pb2
import src.implementation1.gRPC.DataProcessor_pb2_grpc as DataProcessor__pb2_grpc


class LoadBalancerService:
    _stub: DataProcessor__pb2_grpc.DataProcessorServiceStub

    def __init__(self):
        load_dotenv()
        load_balancer_url = '{host}:{port}'.format(host=os.getenv('GRPC_LOAD_BALANCER_HOST'),
                                                   port=os.getenv('GRPC_SERVER_PORT'))
        channel = grpc.insecure_channel(load_balancer_url)
        self._stub = DataProcessor__pb2_grpc.DataProcessorServiceStub(channel)

    def send_meteo_data(self, temperature, humidity, timestamp):
        print(f'Data recived: tmp={str(temperature)} hum={str(humidity)} timestamp={str(timestamp)}')
        self._stub.ProcessMeteoData(
            DataProcessor__pb2.RawMeteoDataP(temperature=temperature, humidity=humidity, timestamp=timestamp))
        return 'Done'

    def send_pollution_data(self, co2, timestamp):
        print(f'Data recived: co2={str(co2)} timestamp={str(timestamp)}')
        self._stub.ProcessPollutionData(
            DataProcessor__pb2.RawPollutionDataP(co2=co2, timestamp=timestamp))
        return 'Done'


lb_service = LoadBalancerService()
