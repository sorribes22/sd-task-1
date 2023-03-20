import time

import grpc
import redis
import os
from dotenv import load_dotenv
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import src.implementation1.gRPC.ClientProxy_pb2_grpc as ClientProxy__pb2_grpc
import src.implementation1.gRPC.ClientProxy_pb2 as ClientProxy__pb2


class Proxy:
    _refresh_time = 2
    _redis: redis.Redis = None
    _terminals = list()

    def _connect_redis(self):
        host = os.getenv('REDIS_HOST')
        port = int(os.getenv('REDIS_PORT'))

        self._redis = redis.Redis(
            host=host,
            port=port
        )

    def _connect_terminals(self):
        terminal_hosts = os.getenv('TERMINAL_HOSTS')
        for kv in terminal_hosts.split(";"):
            url = kv.split(":")
            self._terminals.append(dict(host=url[0], port=url[1]))
        # print(list(kv.split(":") )
        # self._terminals = dict(kv.split(":") for kv in terminal_hosts.split(";"))

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

        self._connect_redis()
        self._connect_terminals()
        load_balancer_url = 'localhost:50100'
        channel = grpc.insecure_channel(load_balancer_url)
        stub = ClientProxy__pb2_grpc.ClientProxyServiceStub(channel)

        while True:
            print('hola')
            stub.SendWellnessResults(self._send_results())
            time.sleep(self._refresh_time)
        # load_dotenv()
        #
        # load_balancer_url = '{host}:{port}'.format(host=os.getenv('GRPC_LOAD_BALANCER_HOST'),
        #                                            port=os.getenv('GRPC_LOAD_BALANCER_PORT')
        #                                            )
        # channel = grpc.insecure_channel(load_balancer_url)
        # stub = ClientProxy__pb2_grpc.LoadBalancerServiceStub(channel)
        #
        # while True:
        #     raw_data = self._data_measured()
        #     func_name = self._grpc_function_name()
        #     try:
        #         func = getattr(stub, func_name)
        #         func(raw_data)
        #     except AttributeError:
        #         print(f"{func_name} not found")
        #
        #     time.sleep(random.randrange(1, 3))


proxy = Proxy()
proxy.start()
