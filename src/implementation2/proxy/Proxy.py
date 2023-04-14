import json
import time
import redis
import numpy
from src.Configuration import Configuration
import pika as pika
from pika.adapters.blocking_connection import BlockingChannel


class Proxy:
    _refresh_time = 5
    _redis: redis.Redis = None
    _channel: BlockingChannel

    def _connect_redis(self):
        self._redis = redis.Redis(
            host=Configuration.get('redis')['host'],
            port=Configuration.get('redis')['port']
        )

    def _connect_terminals_rabbitmq(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Configuration.get('rabbitmq')['host'],
            port=Configuration.get('rabbitmq')['port'],
            credentials=pika.PlainCredentials(
                Configuration.get('rabbitmq')['user'],
                Configuration.get('rabbitmq')['password'])
        ))
        self._channel = connection.channel()
        self._channel.exchange_declare(exchange='broadcast', exchange_type='fanout')

    def _calculate_mean(self, keys: list) -> float:
        values = list(map(float, self._redis.mget(*keys)))
        self._redis.delete(*keys)
        return float(numpy.mean(values))

    def _calculate_pollution(self) -> tuple:
        keys = self._redis.keys('meteo-pollution-*')
        if len(keys) == 0:
            raise Exception('No pollution data found on Redis')
        return self._calculate_mean(keys), keys[-1]

    def _calculate_wellness(self) -> tuple:
        keys = self._redis.keys('meteo-wellness-*')
        return self._calculate_mean(keys), keys[-1]

    def _calculate_result(self) -> dict:
        wellness, air_wellness_at = self._calculate_wellness()
        pollution, pollution_at = self._calculate_pollution()

        air_wellness_at = air_wellness_at[15:]
        pollution_at = pollution_at[16:]
        dispatch_time = (air_wellness_at, pollution_at)[air_wellness_at < pollution_at]
        print("Sending data to Terminal")

        return {
            'air': wellness,
            'co2': pollution,
            'timestamp': dispatch_time.decode('utf-8')
        }

    def start(self):
        self._connect_redis()
        self._connect_terminals_rabbitmq()

        while True:
            try:
                self._channel.basic_publish(
                    exchange='broadcast',
                    routing_key='',
                    body=str(self._calculate_result()).encode()
                )
            except Exception as e:
                pass
            time.sleep(self._refresh_time)
