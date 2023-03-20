import time
import redis
import os
from dotenv import load_dotenv


class Proxy:
    _refresh_time = 2
    _redis: redis.Redis = None

    def _connect_redis(self):
        host = os.getenv('REDIS_HOST')
        port = int(os.getenv('REDIS_PORT'))

        self._redis = redis.Redis(
            host=host,
            port=port
        )

    def start(self):
        load_dotenv()

        self._connect_redis()

        while True:
            print('hola')
            time.sleep(self._refresh_time)


proxy = Proxy()
proxy.start()
