import random
import time
import pika as pika
from pika.adapters.blocking_connection import BlockingChannel
from abc import ABCMeta, abstractmethod
from src.Configuration import Configuration
from src.meteo_utils import MeteoDataDetector


class Sensor(metaclass=ABCMeta):
    _channel: BlockingChannel

    @abstractmethod
    def __init__(self):
        super().__init__()
        self._sensor = MeteoDataDetector()
        self._start_sensor()

    def _data_measured(self) -> bytes:
        """Returns an object with the sensor collected data.

        Returns:
            raw_data (Message): Data measured by sensor
        """
        raise NotImplementedError

    def _rabbitmq_channel_routing_key(self) -> str:
        """Returns on which channel the message should be published.

        Returns:
            Routing key (str): Channel where to publish the message
        """
        raise NotImplementedError

    def _connect_rabbitmq(self) -> None:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Configuration.get('rabbitmq')['host'],
            port=Configuration.get('rabbitmq')['port'],
            credentials=pika.PlainCredentials(
                Configuration.get('rabbitmq')['user'],
                Configuration.get('rabbitmq')['password'])
        ))
        self._channel = connection.channel()
        self._channel.queue_declare(queue='meteo.sensor.air.raw_data')
        self._channel.queue_declare(queue='meteo.sensor.co2.raw_data')

    def _start_sensor(self) -> None:
        self._connect_rabbitmq()

        while True:
            self._channel.basic_publish(
                exchange='',
                routing_key=self._rabbitmq_channel_routing_key(),
                body=self._data_measured()
            )

            time.sleep(random.randrange(1, 3))
