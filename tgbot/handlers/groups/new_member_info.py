from aiogram import Dispatcher
from aiogram.types import ChatMemberUpdated, CallbackQuery
from magic_filter import F

from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.utils.capcha import throw_capcha
from tgbot.config import Config
from tgbot.utils.worker_redis import WorkerRedis, puke_redis
import redis


@logging_message
async def new_member_info(message: ChatMemberUpdated, config: Config) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some use ful links

    """
    redis_users: redis = WorkerRedis(config)
    user_id: int = int(message.new_chat_member.user.id)
    chat_member: bool = message.old_chat_member.is_chat_member()
    if not chat_member:
        if type(message) not in [CallbackQuery]:
            puke_redis(config).add_capcha_flag(user_id, 0)
            await throw_capcha(message=message, config=config)
            logger.info(f"new_member_info run throw capcha {type(message)}\n"
                        f"for user {user_id} ")
        else:
            logger.info(f"new_member_info run in{message.chat.id}\n"
                        f"{type(message)} msg type for no reason\n"
                        f"need FIX (if type(message) not in [CallbackQuery])")
    else:
        logger.info(f"new_member_info run in {message.chat.id}\ntype msg {type(message)}"
                    f" for no reason\n need FIX F.new_chat_member.is_chat_member")


def register_new_member_info(dp: Dispatcher):
    dp.register_chat_member_handler(new_member_info, F.new_chat_member.is_chat_member())
