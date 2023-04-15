import json
from datetime import datetime
from src.Configuration import Configuration
from src.implementation2.sensor.Sensor import Sensor


class PollutionSensor(Sensor):
    def __init__(self):
        super().__init__()

    def _data_measured(self) -> str:
        return json.dumps({
            'co2': self._sensor.gen_co2(),
            'timestamp': datetime.now().strftime(Configuration.get('datetime_format'))
        })

    def _rabbitmq_channel_routing_key(self) -> str:
        return 'meteo.sensor.co2.raw_data'
