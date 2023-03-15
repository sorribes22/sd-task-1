import random
import time

from src.implementation1.meteo_utils import MeteoDataDetector
# from src.implementation1.sensor.RawData import RawData


class Sensor:
    def __init__(self):
        super().__init__()
        self._sensor = MeteoDataDetector()
        # self._start_sensor()

    def _data_measured(self):
        raise NotImplementedError

    def _start_sensor(self) -> None:
        while True:
            raw_data = self._data_measured()
            # self._send_data(raw_data)
            time.sleep(random.randrange(1, 3))

