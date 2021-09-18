import redis

from django.conf import settings


class Redis(object):
    """ """

    reset_password_token_prefix = "reset_password_%s"

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super(Redis, cls).__new__(Redis, *args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        pool = redis.ConnectionPool(
            host=settings.REDIS["host"],
            db=settings.REDIS["db"],
            port=settings.REDIS["port"],
            password=settings.REDIS["password"],
        )

        self._conn = redis.Redis(connection_pool=pool, decode_responses=True)
        self._pipe = self._conn.pipeline()

    def execute(self):
        return self._pipe.execute()

    def set_token(self, user_id, token):
        self._conn.set(
            self.reset_password_token_prefix % user_id,
            token,
            settings.REDIS_TOKEN_EXPIRE_TIME,
        )

    def revoke_token(self, username):
        self._conn.delete(self.reset_password_token_prefix % username)

    def get_token(self, username):
        return self._conn.get(self.reset_password_token_prefix % username)
