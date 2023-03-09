from concurrent import futures
from datetime import time
import grpc

from src.implementation1.gRPC import MeteoServer_pb2
from src.implementation1.gRPC import MeteoServer_pb2_grpc

from src.implementation1.gRPC.LoadBalancerService import lb_service


# create a class to define the server functions
class LoadBalancerServicer(MeteoServer_pb2_grpc.LoadBalancerServiceServicer):

    def SendMeteoData(self, rawMeteoData, context):
        lb_service.send_meteo_data(rawMeteoData.temperature, rawMeteoData.humidity, rawMeteoData.timestamp)
        response = MeteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def SendPollutionData(self, rawPollutionData, context):
        lb_service.send_pollution_data(rawPollutionData.co2, rawPollutionData.timestamp)
        response = MeteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

# create gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

#add the defined class to server
MeteoServer_pb2_grpc.add_LoadBalancerServiceServicer_to_server(LoadBalancerServicer(), server)


print('Starting LoadBalancer. Listening on port 50051')
server.add_insecure_port('0.0.0.0:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)