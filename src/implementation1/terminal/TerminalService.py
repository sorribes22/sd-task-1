from datetime import datetime
from google.protobuf import timestamp_pb2 as _timestamp_pb2


class TerminalService:
    def send_wellness_results(self, air: float, co2: float, timestamp: _timestamp_pb2):
        print(f'Data recived: Air Wellness={str(air)} Pollution={str(co2)} timestamp={str(timestamp)}')
        return 'Done'


terminal_service = TerminalService()
