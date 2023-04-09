import datetime
import threading
import time
import grpc
import redis
import numpy
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import src.implementation1.gRPC.ClientProxy_pb2_grpc as ClientProxy__pb2_grpc
import src.implementation1.gRPC.ClientProxy_pb2 as ClientProxy__pb2
from src.Configuration import Configuration
from datetime import datetime


class Proxy:
    _refresh_time = 5
    _redis: redis.Redis = None
    _terminals: list[ClientProxy__pb2_grpc.ClientProxyServiceStub] = list()

    def _connect_redis(self):
        self._redis = redis.Redis(
            host=Configuration.get('redis')['host'],
            port=Configuration.get('redis')['port']
        )

    def _connect_terminals(self):
        for url_dict in Configuration.get('terminal_urls'):
            url = '{host}:{port}'.format(host=url_dict['host'],
                                         port=url_dict['port'])
            print(f'init {url} stub')
            channel = grpc.insecure_channel(url)
            self._terminals.append(ClientProxy__pb2_grpc.ClientProxyServiceStub(channel))

    def _calculate_mean(self, keys: list) -> float:
        values = list(map(float, self._redis.mget(*keys)))
        self._redis.delete(*keys)
        return float(numpy.mean(values))

    def _calculate_pollution(self) -> tuple:
        keys = self._redis.keys('meteo-pollution-*')
        return self._calculate_mean(keys), keys[-1]

    def _calculate_wellness(self) -> tuple:
        keys = self._redis.keys('meteo-wellness-*')
        return self._calculate_mean(keys), keys[-1]

    def _calculate_result(self):
        wellness, air_wellness_at = self._calculate_wellness()
        pollution, pollution_at = self._calculate_pollution()

        air_wellness_at = air_wellness_at[15:]
        pollution_at = pollution_at[16:]
        dispatch_time = (air_wellness_at, pollution_at)[air_wellness_at < pollution_at]
        dt = datetime.strptime(dispatch_time.decode('utf-8'), '%Y-%m-%d %H:%M:%S.%f')
        timestamp = _timestamp_pb2.Timestamp()
        timestamp.FromDatetime(dt)

        return ClientProxy__pb2.WellnessData(
            air=wellness,
            co2=pollution,
            timestamp=timestamp
        )

    def start(self):
        self._connect_redis()
        self._connect_terminals()

        while True:
            # TODO multithreading
            i = 1
            result = self._calculate_result()
            print('sending messages...')
            for stub in self._terminals:
                print(f'to terminal {i}')
                i += 1
                stub.SendWellnessResults(result)
            time.sleep(self._refresh_time)
