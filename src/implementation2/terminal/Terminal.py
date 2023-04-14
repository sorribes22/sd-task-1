import time
import json
from src.Configuration import Configuration
import pika
from types import SimpleNamespace
from pika.adapters.blocking_connection import BlockingChannel


class Terminal:
    _channel: BlockingChannel

    def _get_key(self, prefix: str, raw_data):
        return prefix + raw_data.timestamp

    def _print_data(self, ch, method, properties, body):
        print(body)

    def _connect_rabbitmq(self) -> str:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Configuration.get('rabbitmq')['host'],
            port=Configuration.get('rabbitmq')['port'],
            credentials=pika.PlainCredentials(
                Configuration.get('rabbitmq')['user'],
                Configuration.get('rabbitmq')['password'])
        ))
        self._channel = connection.channel()
        self._channel.exchange_declare(exchange='satilla', exchange_type='fanout')
        result = self._channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self._channel.queue_bind(exchange='satilla', queue=queue_name)
        return queue_name

    def start(self):
        queue_name = self._connect_rabbitmq()
        print("Start terminal : ", queue_name)
        self._channel.basic_consume(queue=queue_name, on_message_callback=self._print_data, auto_ack=True)
        self._channel.start_consuming()
