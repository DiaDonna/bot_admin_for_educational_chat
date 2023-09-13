from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ChatMemberUpdated
from magic_filter import F

from tgbot.utils.decorators import logging_message
from tgbot.utils.log_config import logger
from tgbot.utils.texts import greeting_text


@logging_message
async def new_member_info(message: ChatMemberUpdated) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """

    bot_user = await message.bot.get_me()
    greeting: str = greeting_text(message=message, bot_user=bot_user)

    await message.bot.send_message(chat_id=message.chat.id, disable_web_page_preview=True, text=greeting, reply_markup=ReplyKeyboardRemove())
    logger.info("New User {user} was greeting".format(
        user=message.new_chat_member.user.id)
    )


def register_new_member_info(dp: Dispatcher):
    dp.register_chat_member_handler(new_member_info, F.new_chat_member.is_chat_member())
