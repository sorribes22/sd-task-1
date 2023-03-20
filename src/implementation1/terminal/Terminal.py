import time
import grpc
import os
import src.implementation1.gRPC.ClientProxy_pb2 as ClientProxy__pb2
import src.implementation1.gRPC.ClientProxy_pb2_grpc as ClientProxy__pb2_grpc
from concurrent import futures
from TerminalService import terminal_service
from dotenv import load_dotenv


# create a class to define the server functions
class Terminal(ClientProxy__pb2_grpc.ClientProxyServiceServicer):

    def SendWellnessResults(self, wellness_data, context):
        terminal_service.send_wellness_results(wellness_data.air, wellness_data.co2, wellness_data.timestamp)
        response = ClientProxy__pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


# create gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# add the defined class to server
ClientProxy__pb2_grpc.add_ClientProxyServiceServicer_to_server(Terminal(), server)

load_dotenv()
print('Starting LoadBalancer. Listening on port {host}'.format(host=50100))
server.add_insecure_port('0.0.0.0:{host}'.format(host=50100))
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
