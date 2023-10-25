import redis
from tgbot.config import Config


with redis.Redis(host='localhost', port=6379, decode_responses=True) as redis:
    redis.hset('users_capcha_key_dict', mapping={'1234': 'Bill'})
    redis.hset('users_captcha_flag_dict', mapping={'1234': 1})
    print(redis.hget('users_captcha_flag_dict', '1234'))
    redis.hset('users_captcha_flag_dict', mapping={'1234': 0})
    print(redis.hget('users_captcha_flag_dict', '1234'))
    redis.hset('users_capcha_key_dict', mapping={'6237': 'Hoi'})
    print(redis.hkeys('users_capcha_key_dict'))
    print(redis.hkeys('users_captcha_flag_dict'))
    #redis.hdel('users_capcha_key_dict', ['1234'])
    print(redis.hgetall('users_capcha_key_dict'))
    redis.hdel('users_capcha_key_dict', '1234')
    print(redis.hgetall('users_capcha_key_dict'))
