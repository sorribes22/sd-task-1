import json
import pika
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from src.Configuration import Configuration
from pika.adapters.blocking_connection import BlockingChannel


class Terminal:
    _channel: BlockingChannel

    def _get_key(self, prefix: str, raw_data):
        return prefix + raw_data.timestamp

    def _print_data(self, ch, method, properties, body):
        text = body.decode('utf-8')
        dic = json.loads(text.replace("'", "\""))
        air = dic['air']
        co2 = dic['co2']
        time_s = dic['timestamp']
        print(f"Air: {Fore.GREEN}{air:.3f}{Style.RESET_ALL}, CO2: {Fore.RED}{co2:.3f}{Style.RESET_ALL} - Timestamp: {time_s}")

    def _connect_rabbitmq(self) -> str:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Configuration.get('rabbitmq')['host'],
            port=Configuration.get('rabbitmq')['port'],
            credentials=pika.PlainCredentials(
                Configuration.get('rabbitmq')['user'],
                Configuration.get('rabbitmq')['password'])
        ))
        self._channel = connection.channel()
        self._channel.exchange_declare(exchange='broadcast', exchange_type='fanout')
        result = self._channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self._channel.queue_bind(exchange='broadcast', queue=queue_name)
        return queue_name

    def start(self):
        colorama_init()

        queue_name = self._connect_rabbitmq()
        print("Start terminal, Queue name : ", queue_name)
        self._channel.basic_consume(queue=queue_name, on_message_callback=self._print_data, auto_ack=True)
        self._channel.start_consuming()
