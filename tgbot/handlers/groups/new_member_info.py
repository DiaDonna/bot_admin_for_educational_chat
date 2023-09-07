
from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes

from tgbot.config import Config
from tgbot.utils.decorators import logging_message
from tgbot.utils.capcha import throw_capcha


@logging_message
async def new_member_info(message: Message, config: Config) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """
    await throw_capcha(message, config)


def register_new_member_info(dp: Dispatcher):
    dp.register_message_handler(new_member_info,
                                content_types=ContentTypes.NEW_CHAT_MEMBERS)
