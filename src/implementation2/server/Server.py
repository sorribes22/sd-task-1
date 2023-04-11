import time
from datetime import datetime

import pika
import json

import redis
from pika.adapters.blocking_connection import BlockingChannel
from types import SimpleNamespace
from src.Configuration import Configuration
from src.meteo_utils import MeteoDataProcessor


class Server:
    _meteo_data_processor: MeteoDataProcessor
    _redis: redis.Redis = None
    _channel: BlockingChannel

    def __init__(self):
        self._meteo_data_processor = MeteoDataProcessor()

    def _connect_redis(self):
        self._redis = redis.Redis(
            host=Configuration.get('redis')['host'],
            port=Configuration.get('redis')['port']
        )

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

    def _get_key(self, prefix: str, raw_data):
        return prefix + raw_data.timestamp

    def _parse_message(self, body):
        data = json.loads(body)
        data = SimpleNamespace(**data)
        return data

    def _process_meteo_data(self, ch, method, properties, body):
        data = self._parse_message(body)
        result = self._meteo_data_processor.process_meteo_data(data)
        key = self._get_key('meteo-wellness-', data)
        self._redis.set(key, result)

    def _process_pollution_data(self, ch, method, properties, body):
        data = self._parse_message(body)
        result = self._meteo_data_processor.process_pollution_data(data)
        key = self._get_key('meteo-pollution-', data)
        self._redis.set(key, result)

    def start_server(self):
        self._connect_redis()
        self._connect_rabbitmq()

        self._channel.basic_consume(queue='meteo.sensor.air.raw_data',
                                    on_message_callback=self._process_meteo_data,
                                    auto_ack=True)
        self._channel.basic_consume(queue='meteo.sensor.co2.raw_data',
                                    on_message_callback=self._process_pollution_data,
                                    auto_ack=True)
        self._channel.start_consuming()
