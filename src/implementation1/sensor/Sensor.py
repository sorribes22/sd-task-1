from src.implementation1.meteo_utils import MeteoDataDetector


class Sensor(MeteoDataDetector):
    def __init__(self):
        super().__init__()
        self._sensor = MeteoDataDetector()