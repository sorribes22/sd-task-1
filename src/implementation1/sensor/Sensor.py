import random
import time
import os
import grpc
import src.implementation1.gRPC.MeteoServer_pb2_grpc as MeteoServer__pb2_grpc
from abc import ABCMeta, abstractmethod
from dotenv import load_dotenv
from src.implementation1.meteo_utils import MeteoDataDetector


class Sensor(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self._sensor = MeteoDataDetector()
        self._start_sensor()

    def _data_measured(self):
        raise NotImplementedError

    def _start_sensor(self) -> None:
        load_dotenv()

        rabbitmq_url = '{host}:{port}'.format(host=os.getenv('RABBITMQ_HOST'),
                                              port=os.getenv('RABBITMQ_PORT')
                                              )
        channel = grpc.insecure_channel(rabbitmq_url)
        stub = MeteoServer__pb2_grpc.LoadBalancerServiceStub(channel)

        while True:
            raw_data = self._data_measured()
            stub.SendMeteoData(raw_data)
            time.sleep(random.randrange(1, 3))
