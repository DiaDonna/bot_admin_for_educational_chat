from aiogram import Dispatcher, types
from aiogram.types import Message

from tgbot.utils.log_config import logger
from tgbot.utils.texts import greeting_text


async def new_member_info(message: Message) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """

    bot_user = await message.bot.get_me()
    greeting: str = greeting_text(message=message, bot_user=bot_user)

    await message.answer(text=greeting, disable_web_page_preview=True)
    logger.info("New User {user} was greeting".format(
        user=message.new_chat_members[0].id)
    )


def register_new_member_info(dp: Dispatcher):
    dp.register_message_handler(new_member_info,
                                content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
