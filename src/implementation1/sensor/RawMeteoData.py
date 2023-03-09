from datetime import datetime
from src.implementation1.sensor.RawData import RawData


class RawMeteoData(RawData):
    temperature: float
    humidity: float
    timestamp: datetime
