from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ChatMemberUpdated
from magic_filter import F

from tgbot.utils.decorators import logging_message
from tgbot.utils.log_config import logger
from tgbot.utils.texts import greeting_text
from tgbot.utils.capcha import throw_capcha
from tgbot.config import Config


@logging_message
async def new_member_info(message: ChatMemberUpdated, config: Config) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """
    await throw_capcha(message=message, config=config)


def register_new_member_info(dp: Dispatcher):
    dp.register_chat_member_handler(new_member_info, F.new_chat_member.is_chat_member())
