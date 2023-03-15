from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
class LoadBalancerService:
    def send_meteo_data(self, temperature, humidity, timestamp):
        seconds = timestamp.ToSeconds()
        nanos = timestamp.ToNanoseconds()
        proto_timestamp = Timestamp(seconds=seconds, nanos=nanos)
        print((Timestamp(timestamp)).ToDatetime())
        print(datetime.fromtimestamp(timestamp))
        print('Data recived: tmp={tmp} hum={hum} time={time}'.format(
            tmp=str(temperature),
            hum=str(humidity),
            time=str(timestamp)
        ))
        return 'Done'

    def send_pollution_data(self, co2, timestamp):
        print('Data recived' + co2 + ' ' + timestamp)
        return 'Done'


lb_service = LoadBalancerService()
