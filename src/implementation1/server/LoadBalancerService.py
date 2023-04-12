import os
from datetime import datetime

import grpc
from dotenv import load_dotenv
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import src.implementation1.gRPC.DataProcessor_pb2 as DataProcessor__pb2
import src.implementation1.gRPC.DataProcessor_pb2_grpc as DataProcessor__pb2_grpc

from src.implementation1.server.RoundRobinLoadBalancer import RoundRobinLoadBalancer


class LoadBalancerService:
    _load_balancer: RoundRobinLoadBalancer()

    def __init__(self):
        load_dotenv()
        self._load_balancer = RoundRobinLoadBalancer()
        server_hosts = os.getenv('GRPC_SERVER_PORTS')
        for sh in server_hosts.split(";"):
            channel = grpc.insecure_channel(sh)
            self._load_balancer.append_stub(DataProcessor__pb2_grpc.DataProcessorServiceStub(channel))

    def send_meteo_data(self, temperature, humidity, timestamp):
        # print(f'LB Data recived: tmp={str(temperature)} hum={str(humidity)} timestamp={str(timestamp)}')
        stub = self._load_balancer.get_stub()
        call_future = stub.ProcessMeteoData.future(
            DataProcessor__pb2.RawMeteoDataP(temperature=temperature, humidity=humidity, timestamp=timestamp))
        self._load_balancer.append_stub(stub)
        return 'Done'

    def send_pollution_data(self, co2, timestamp):
        # print(f'LB Data recived: co2={str(co2)} timestamp={str(timestamp)}')
        stub = self._load_balancer.get_stub()
        call_future = stub.ProcessPollutionData.future(
            DataProcessor__pb2.RawPollutionDataP(co2=co2, timestamp=timestamp))
        self._load_balancer.append_stub(stub)
        return 'Done'


lb_service = LoadBalancerService()
