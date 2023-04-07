import time

import grpc
import redis
import os
from dotenv import load_dotenv
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import src.implementation1.gRPC.ClientProxy_pb2_grpc as ClientProxy__pb2_grpc
import src.implementation1.gRPC.ClientProxy_pb2 as ClientProxy__pb2
from src.Configuration import Configuration


class Proxy:
    _refresh_time = 2
    _redis: redis.Redis = None
    _terminals: list[ClientProxy__pb2_grpc.ClientProxyServiceStub] = list()

    def _connect_redis(self):
        host = os.getenv('REDIS_HOST')
        port = int(os.getenv('REDIS_PORT'))

        self._redis = redis.Redis(
            host=host,
            port=port
        )

    def _connect_terminals(self):
        for url_dict in Configuration.get('terminal_urls'):
            url = '{host}:{port}'.format(host=url_dict['host'],
                                         port=url_dict['port'])
            print(f'init {url} stub')
            channel = grpc.insecure_channel(url)
            self._terminals.append(ClientProxy__pb2_grpc.ClientProxyServiceStub(channel))

    def _send_results(self):

        ts = _timestamp_pb2.Timestamp()
        ts.GetCurrentTime()
        return ClientProxy__pb2.WellnessData(
            air=1.0,
            co2=1.0,
            timestamp=ts
        )

    def start(self):
        load_dotenv()

        # self._connect_redis()
        self._connect_terminals()

        while True:
            # TODO multithreading
            i = 1
            result = self._send_results()
            print('sending messages...')
            for stub in self._terminals:
                print(f'to terminal {i}')
                i += 1
                stub.SendWellnessResults(result)
            time.sleep(self._refresh_time)
