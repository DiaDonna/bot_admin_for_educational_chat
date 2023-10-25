import redis
from tgbot.config import Config


class RedisHandler:
    """
        Class: work with redis context manager
        init:  config(host, port)
        type work for redis
        with redis.Redis(host='localhost', port=6379, decode_responses=True) as redis:
             redis.hset('users_capcha_key_dict', mapping={'1234': '1123'}) set map conf
             redis.hset('users_capcha_flag_dict', mapping={'1234': 1}) set map flag
             redis.hget('users_capcha_flag_dict', '1234') get flag
             redis.hset('users_capcha_flag_dict', mapping={'1234': 0}) change flag
             redis.hset('users_capcha_key_dict', mapping={'6237': '111'}) add to map conf
             redis.hkeys('users_capcha_key_dict') get keys
             redis.hdel('users_capcha_key_dict', ['1234']) del elem
             redis.hgetall('users_capcha_key_dict') get map
    """

    def __int__(self, config: Config):
        self.host: str = config.redis.redis_host_name
        self.port: int = config.redis.redis_port
        self.user_map_name: str = 'users_capcha_key_map'
        self.users_capcha_flag_map: str = 'users_capcha_flag_map'

    def add_capcha_key(self, user_id: int, capcha: int):
        with redis.Redis(host=self.host, port=self.port, decode_responses=True) as r:
            r.hset(self.user_map_name, mapping={str(user_id): capcha})

    def del_capcha_key(self, user_id: int):
        with redis.Redis(host=self.host, port=self.port, decode_responses=True) as r:
            r.hdel(self.user_map_name, str(user_id))

    def add_capcha_flag(self, user_id: int, flag: int):
        with redis.Redis(host=self.host, port=self.port, decode_responses=True) as r:
            r.hset(self.users_capcha_flag_map, mapping={str(user_id): flag})

    def change_capcha_flag(self, user_id: int, flag: int):
        with redis.Redis(host=self.host, port=self.port, decode_responses=True) as r:
            r.hset(self.users_capcha_flag_map, mapping={str(user_id): flag})

    def del_capcha_flag(self, user_id: int):
        with redis.Redis(host=self.host, port=self.port, decode_responses=True) as r:
            r.hdel(self.users_capcha_flag_map, str(user_id))
