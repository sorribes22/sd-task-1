import itertools
import src.implementation1.gRPC.DataProcessor_pb2_grpc as DataProcessor__pb2_grpc


class RoundRobinLoadBalancer:
    _stubs: list[DataProcessor__pb2_grpc.DataProcessorServiceStub] = list()

    def get_stub(self) -> DataProcessor__pb2_grpc.DataProcessorServiceStub:
        return self._stubs.pop(0)

    def append_stub(self, stub: DataProcessor__pb2_grpc.DataProcessorServiceStub):
        self._stubs.append(stub)
