from babel.dates import format_timedelta
from datetime import timedelta

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest


from tgbot.utils.chat_t import chat_types
from tgbot.utils.decorators import admin_and_bot_check
from tgbot.utils.log_config import logger
from tgbot.utils.timedelta import parse_timedelta_from_message
from tgbot.utils.update_log import add_to_log_message


async def ro(message: Message) -> None:
    """
    Хендлер для команды !ro для роли ADMIN

    Команда позволяет перевести пользователя в режим "только чтение" с указанием продолжительности ограничения.
    Команду необходимо писать в ответе пересылаемого сообщения от того пользователя, которого нужно забанить.

    Command can be used for turning on mode read-only for users, you can write duration of this restriction.
    You should write this command in response to a message from the user you want to block.
    """

    await add_to_log_message(message=message)
    duration: timedelta = await parse_timedelta_from_message(message)
    if not duration:
        return

    try:
        await message.chat.restrict(message.reply_to_message.from_user.id, can_send_messages=False, until_date=duration)
        logger.info("User {user} restricted by {admin} for {duration}".format(
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id,
            duration=duration)
        )
        await message.reply_to_message.answer(
            "<b>Режим &#171;только чтениe&#187;</b> активирован для пользователя {user}."
            "\nПродолжительность: {duration}".format(
                user=message.reply_to_message.from_user.get_mention(),
                duration=format_timedelta(duration, locale='ru', granularity="second", format="short"))
        )

    except BadRequest as e:
        logger.error("Failed to restrict chat member: {error!r}", exc_info=e)


def register_ro(dp: Dispatcher) -> None:
    dp.register_message_handler(admin_and_bot_check(ro),
                                is_reply=True,
                                chat_type=chat_types(),
                                commands=["ro"],
                                commands_prefix='!',
                                state="*",
                                is_admin=True)
