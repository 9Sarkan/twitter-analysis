import redis
from helpers.utils import get_env


class Client(object):
    """ """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super(Client, cls).__new__(Client, *args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        pool = redis.ConnectionPool(
            host=get_env("REDIS_HOST", default="localhost"),
            db=get_env("REDIS_DB", default=0),
            port=int(get_env("REDIS_PORT", default=6379)),
        )

        self._conn = redis.Redis(connection_pool=pool, decode_responses=True)
        self._pipe = self._conn.pipeline()

    def execute(self):
        return self._pipe.execute()

    def add_to_list(self, list_name, item):
        self._conn.zincrby(list_name, 1, item)

    def remove_from_list(self, list_name, item):
        return self._conn.zrem(list_name, item)

    def get_most_common(self, list_name, most_common):
        return self._conn.zrevrange(list_name, 0, most_common - 1)
