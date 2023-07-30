
from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove, User

from tgbot.utils.decorators import logging_message
from tgbot.utils.log_config import logger
from tgbot.utils.texts import greeting_text
from tgbot.handlers.groups.throw_entry_captcha import captcha


@logging_message
async def new_member_info(message: Message) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """

    bot_user: User = await message.bot.get_me()
    greeting: str = greeting_text(message=message, bot_user=bot_user)
    user_id: str = message.new_chat_members[0].id

    await message.answer(text=greeting, disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
    logger.info(f"New User {user_id} was greeting")
    await captcha(message)


def register_new_member_info(dp: Dispatcher):
    dp.register_message_handler(new_member_info,
                                content_types=ContentTypes.NEW_CHAT_MEMBERS)
