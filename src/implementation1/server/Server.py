import time
import grpc
from concurrent import futures
import redis
import src.implementation1.gRPC.DataProcessor_pb2 as DataProcessor__pb2
import src.implementation1.gRPC.DataProcessor_pb2_grpc as DataProcessor__pbs_grpc
from src.Configuration import Configuration
from src.meteo_utils import MeteoDataProcessor


class Server(DataProcessor__pbs_grpc.DataProcessorServiceServicer):
    _port: int
    _meteo_data_processor: MeteoDataProcessor
    _redis: redis.Redis = None

    def __init__(self, port: int):
        self._port = port
        self._meteo_data_processor = MeteoDataProcessor()

    def _connect_redis(self):
        self._redis = redis.Redis(
            host=Configuration.get('redis')['host'],
            port=Configuration.get('redis')['port']
        )

    def _get_key(self, prefix: str, raw_data):
        return prefix + raw_data.timestamp.ToDatetime().strftime('%Y-%m-%d %H:%M:%S.%f')

    def ProcessMeteoData(self, raw_meteo_data_p, context):
        result = self._meteo_data_processor.process_meteo_data(raw_meteo_data_p)
        key = self._get_key('meteo-wellness-', raw_meteo_data_p)
        self._redis.set(key, result)
        return DataProcessor__pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def ProcessPollutionData(self, raw_pollution_data_p, context):
        result = self._meteo_data_processor.process_pollution_data(raw_pollution_data_p)
        key = self._get_key('meteo-pollution-', raw_pollution_data_p)
        self._redis.set(key, result)
        return DataProcessor__pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def start_server(self):
        self._connect_redis()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        DataProcessor__pbs_grpc.add_DataProcessorServiceServicer_to_server(self, server)

        print('Starting Server. Listening on port {host}'.format(host=self._port))
        server.add_insecure_port('0.0.0.0:{host}'.format(host=self._port))
        server.start()

        # since server.start() will not block,
        # a sleep-loop is added to keep alive
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)


# s = Server(20001)
# s.start_server()
