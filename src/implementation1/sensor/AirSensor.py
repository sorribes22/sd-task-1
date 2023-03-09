from src.implementation1.sensor.RawMeteoData import RawMeteoData
from src.implementation1.sensor.Sensor import Sensor


class AirSensor(Sensor):
    def _data_measured(self) -> RawMeteoData:
        return
