import logging
from babel.dates import format_timedelta
from datetime import timedelta
from magic_filter import F

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest

from tgbot.filters.admin import AdminFilter
from tgbot.utils.chat_t import chat_types
from tgbot.utils.timedelta import parse_timedelta_from_message


async def ro(message: Message) -> None:
    """
    Хендлер для команды !ro для роли ADMIN

    Команда позволяет перевести пользователя в режим "только чтение" с указанием продолжительности ограничения.
    Команду необходимо писать в ответе пересылаемого сообщения от того пользователя, которого нужно забанить.

    Command can be used for turning on mode read-only for users, you can write duration of this restriction.
    You should write this command in response to a message from the user you want to block.
    """
    logger = logging.getLogger(__name__)

    is_bot: bool = message.reply_to_message.from_user.is_bot
    is_admin: bool = await AdminFilter.check(message.reply_to_message)
    if is_admin or is_bot:
        await message.reply_to_message.answer(text=f'{message.from_user.get_mention()}, '
                                                   f'вы не можете ограничить бота, владельца или администратора чата!')
        return

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
    dp.register_message_handler(ro,
                                F.ilter(F.reply_to_message),
                                chat_type=chat_types(),
                                commands=["ro"],
                                commands_prefix='!',
                                state="*",
                                is_admin=True)
