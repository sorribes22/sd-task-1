from datetime import datetime
from google.protobuf import timestamp_pb2 as _timestamp_pb2


class LoadBalancerService:
    def send_meteo_data(self, temperature, humidity, timestamp):
        #print(datetime.fromtimestamp(timestamp))
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
