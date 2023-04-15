import random
import time
import grpc
import src.implementation1.gRPC.MeteoServer_pb2_grpc as MeteoServer__pb2_grpc
from abc import ABCMeta, abstractmethod
from google.protobuf import message as _message
from src.Configuration import Configuration
from src.meteo_utils import MeteoDataDetector


class Sensor(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self._sensor = MeteoDataDetector()
        self._start_sensor()

    def _data_measured(self) -> _message.Message:
        """Returns an object with the sensor collected data.

        Returns:
            raw_data (Message): Data measured by sensor
        """
        raise NotImplementedError

    def _grpc_function_name(self) -> str:
        """Returns which gRPC function should be called.

        Returns:
            function_name (str): Function to be called on gRPC server
        """
        raise NotImplementedError

    def _start_sensor(self) -> None:
        load_balancer_url = '{host}:{port}'.format(host=Configuration.get('load_balancer_url')['host'],
                                                   port=Configuration.get('load_balancer_url')['port']
                                                   )
        channel = grpc.insecure_channel(load_balancer_url)
        stub = MeteoServer__pb2_grpc.LoadBalancerServiceStub(channel)

        while True:
            raw_data = self._data_measured()
            func_name = self._grpc_function_name()
            try:
                func = getattr(stub, func_name)
                func(raw_data)
            except AttributeError:
                print(f"{func_name} not found")

            time.sleep(random.randrange(1, 3))
