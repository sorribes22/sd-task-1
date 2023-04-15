import os

from dotenv import load_dotenv


class Configuration:
    _config: dict = dict()
    _instance = None

    def __init__(self):
        self.reload_env_file()

    def reload_env_file(self):
        load_dotenv()

        self._config.update({'datetime_format': '%Y-%m-%d %H:%M:%S.%f'})

        terminal_hosts = os.getenv('TERMINAL_HOSTS')
        self._config.update({'terminal_urls': []})
        for kv in terminal_hosts.split(";"):
            url = kv.split(":")
            self._config.get('terminal_urls').append(dict(host=url[0], port=url[1]))

        self._config.update({'redis': dict(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT')
        )})

        self._config.update({'rabbitmq': dict(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=os.getenv('RABBITMQ_PORT', 5672),
            user=os.getenv('RABBITMQ_USER'),
            password=os.getenv('RABBITMQ_PASSWORD')
        )})

        self._config.update({'load_balancer_url': dict(
            host=os.getenv('GRPC_LOAD_BALANCER_HOST'),
            port=os.getenv('GRPC_LOAD_BALANCER_PORT')
        )})

        terminal_hosts = os.getenv('GRPC_SERVER_PORTS')
        self._config.update({'grpc_server_urls': []})
        for kv in terminal_hosts.split(";"):
            self._config.get('grpc_server_urls').append(kv)

    @staticmethod
    def _get_instance():
        if Configuration._instance is None:
            Configuration._instance = Configuration()
        return Configuration._instance

    def get_configuration(self) -> dict:
        return self._config

    @staticmethod
    def get(key: str):
        return Configuration._get_instance().get_configuration()[key]
