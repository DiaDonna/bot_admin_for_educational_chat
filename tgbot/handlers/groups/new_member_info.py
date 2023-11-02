from aiogram import Dispatcher
from aiogram.types import ChatMemberUpdated, CallbackQuery, ReplyKeyboardRemove
from magic_filter import F

from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.utils.capcha import throw_capcha
from tgbot.config import Config
from tgbot.utils.worker_redis import WorkerRedis
import redis


@logging_message
async def new_member_info(message: ChatMemberUpdated, config: Config) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some use ful links

    """
    # user_id: int = int(message.new_chat_member.user.id)
    # TODO Try another
    redis_users: redis = WorkerRedis(config)
    list_users_redis: list[int] = list(map(int, redis_users.get_all_capcha_user_key()))
    user_id: int = int(message.new_chat_member.user.id)
    if user_id not in list_users_redis:
        if type(message) is not CallbackQuery:
            redis_users.add_capcha_flag(user_id, 0)
            await throw_capcha(message=message, config=config)
        else:
            logger.info(f"new_member_info run in {type(message)}")
    else:
        logger.info(f"new_member_info run in {message.chat.id}")


def register_new_member_info(dp: Dispatcher):
    dp.register_chat_member_handler(new_member_info, F.new_chat_member.is_chat_member())
