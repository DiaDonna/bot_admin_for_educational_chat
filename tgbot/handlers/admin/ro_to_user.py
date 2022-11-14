import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest
from babel.dates import format_timedelta
from magic_filter import F

from tgbot.utils.chat_t import chat_types
from tgbot.utils.timedelta import parse_timedelta_from_message


async def ro(message: Message) -> None:
    logger = logging.getLogger(__name__)
    duration = await parse_timedelta_from_message(message)
    if not duration:
        return

    try:  # Apply restriction
        await message.chat.restrict(
            message.reply_to_message.from_user.id, can_send_messages=False, until_date=duration
        )
        logger.info("User {user} restricted by {admin} for {duration}".format(
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id,
            duration=duration)
        )
    except BadRequest as e:
        logger.error("Failed to restrict chat member: {error!r}", exc_info=e)

    await message.reply_to_message.answer(
        "<b>Режим только чтения</b> активирован для пользователя {user}. Продолжительность: {duration}".format(
            user=message.reply_to_message.from_user.get_mention(),
            duration=format_timedelta(
                duration, locale='ru', granularity="second", format="short"
            ),
        )
    )


def register_ro(dp: Dispatcher) -> None:
    dp.register_message_handler(ro,
                                F.ilter(F.reply_to_message),
                                chat_type=chat_types(),
                                commands=["ro"],
                                commands_prefix='!',
                                state="*",
                                is_admin=True)
