import os
import time
import grpc
from concurrent import futures

from dotenv import load_dotenv

import src.implementation1.gRPC.DataProcessor_pb2 as DataProcessor__pb2
import src.implementation1.gRPC.DataProcessor_pb2_grpc as DataProcessor__pbs_grpc
from src.implementation1.server.ServerService import server_service


class Server(DataProcessor__pbs_grpc.DataProcessorServiceServicer):
    _port: int

    def __init__(self, port: int):
        self._port = port

    def ProcessMeteoData(self, raw_meteo_data_p, context):
        server_service.process_meteo_data(raw_meteo_data_p.temperature, raw_meteo_data_p.humidity,
                                          raw_meteo_data_p.timestamp)
        response = DataProcessor__pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def ProcessPollutionData(self, raw_pollution_data_p, context):
        server_service.process_pollution_data(raw_pollution_data_p.co2, raw_pollution_data_p.timestamp)
        response = DataProcessor__pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def start_server(self):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        DataProcessor__pbs_grpc.add_DataProcessorServiceServicer_to_server(self, server)

        load_dotenv()
        rabbitmq_port = os.getenv('GRPC_SERVER_PORT')
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
