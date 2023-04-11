import json
from datetime import datetime
from src.Configuration import Configuration
from src.implementation2.sensor.Sensor import Sensor


class AirSensor(Sensor):
    def __init__(self):
        super().__init__()

    def _data_measured(self) -> str:
        return json.dumps({
            'temperature': self._sensor.gen_temperature(),
            'humidity': self._sensor.gen_humidity(),
            'timestamp': datetime.now().strftime(Configuration.get('datetime_format'))
        })

    def _rabbitmq_channel_routing_key(self) -> str:
        return 'meteo.sensor.air.raw_data'

# AirSensor()
