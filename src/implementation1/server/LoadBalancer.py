import time
import grpc
import os
import src.implementation1.gRPC.MeteoServer_pb2 as MeteoServer__pb2
import src.implementation1.gRPC.MeteoServer_pb2_grpc as MeteoServer__pb2_grpc
from concurrent import futures
from LoadBalancerService import lb_service
from dotenv import load_dotenv


# create a class to define the server functions
class LoadBalancerServicer(MeteoServer__pb2_grpc.LoadBalancerServiceServicer):

    def SendMeteoData(self, raw_meteo_data, context):
        lb_service.send_meteo_data(raw_meteo_data.temperature, raw_meteo_data.humidity, raw_meteo_data.timestamp)
        response = MeteoServer__pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def SendPollutionData(self, raw_pollution_data, context):
        lb_service.send_pollution_data(raw_pollution_data.co2, raw_pollution_data.timestamp)
        response = MeteoServer__pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


# create gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# add the defined class to server
MeteoServer__pb2_grpc.add_LoadBalancerServiceServicer_to_server(LoadBalancerServicer(), server)

load_dotenv()
rabbitmq_port = os.getenv('RABBITMQ_PORT')
print('Starting LoadBalancer. Listening on port {host}'.format(host=rabbitmq_port))
server.add_insecure_port('0.0.0.0:{host}'.format(host=rabbitmq_port))
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
