import asyncio

from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove, User

from tgbot.config import Config
from tgbot.utils.decorators import logging_message
from tgbot.utils.log_config import logger
from tgbot.utils.texts import greeting_text
from tgbot.handlers.groups.throw_entry_captcha import handler_throw_captcha


@logging_message
async def new_member_info(message: Message, config: Config) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """
    # TODO need solve of bag new_user != user_id
    bot_user: User = await message.bot.get_me()
    greeting: str = greeting_text(message=message, bot_user=bot_user)
    user_id: int = message.new_chat_members[0].id

    msg: Message = await message.answer(text=greeting, disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
    logger.info(f"New User {user_id} was greeting")
    await handler_throw_captcha(message, config)
    await asyncio.sleep(config.time_delta.time_rise_asyncio_del_msg)
    await msg.delete()


def register_new_member_info(dp: Dispatcher):
    dp.register_message_handler(new_member_info,
                                content_types=ContentTypes.NEW_CHAT_MEMBERS)
