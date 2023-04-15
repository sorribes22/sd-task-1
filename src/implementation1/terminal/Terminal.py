import time
import grpc
import src.implementation1.gRPC.ClientProxy_pb2 as ClientProxy__pb2
import src.implementation1.gRPC.ClientProxy_pb2_grpc as ClientProxy__pb2_grpc
from concurrent import futures


class Terminal(ClientProxy__pb2_grpc.ClientProxyServiceServicer):
    _port: int

    def __init__(self, port: int):
        self._port = port

    def SendWellnessResults(self, wellness_data, context):
        print(f'Data recived: Air Wellness={str(wellness_data.air)} Pollution={str(wellness_data.co2)} timestamp={str(wellness_data.timestamp)}')
        response = ClientProxy__pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def start(self):
        # create gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # add the defined class to server
        ClientProxy__pb2_grpc.add_ClientProxyServiceServicer_to_server(self, server)

        print('Starting LoadBalancer. Listening on port {port}'.format(port=self._port))
        server.add_insecure_port('0.0.0.0:{port}'.format(port=self._port))
        server.start()

        # since server.start() will not block,
        # a sleep-loop is added to keep alive
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)
