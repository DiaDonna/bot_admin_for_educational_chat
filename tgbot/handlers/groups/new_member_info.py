from aiogram import Dispatcher
from aiogram.types import ChatMemberUpdated
from magic_filter import F

from tgbot.utils.decorators import logging_message
from tgbot.utils.capcha import throw_capcha
from tgbot.config import Config, user_dict


@logging_message
async def new_member_info(message: ChatMemberUpdated, config: Config) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links

    """
    user_id: int = int(message.new_chat_member.user.id)
    if user_id not in [*user_dict.keys()]:
        await throw_capcha(message=message, config=config)


def register_new_member_info(dp: Dispatcher):
    dp.register_chat_member_handler(new_member_info, F.new_chat_member.is_chat_member())
