import asyncio
import logging
from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.utils.exceptions import Unauthorized
from aiogram.utils.markdown import hlink, quote_html
from magic_filter import F

from tgbot.config import Config
from tgbot.utils.chat_t import chat_types


async def text_report_admins(message: types.Message, config: Config):
    """
    Хендлер для команды !report и /report
    Позволяет пользователям пожаловаться на сообщение в чате
    Следует писать только в ответ на сообщение, о котором необходимо сообщить

    Handler for commands !report and /report
    Command can be used for reporting to admins.
    You should write this command in response to a message you to report.
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "User {user} report message {message} in chat {chat} from user {from_user}".format(
            user=message.from_user.id,
            message=message.message_id,
            chat=message.chat.id,
            from_user=message.reply_to_message.from_user.id,
        ))
    if message.reply_to_message.content_type in {ContentType.FORUM_TOPIC_CREATED,
                                                 ContentType.FORUM_TOPIC_REOPENED,
                                                 ContentType.FORUM_TOPIC_CLOSED}:
        return

    if message.chat.username:
        url = f"https://t.me/{message.chat.username}/{message.reply_to_message.message_id}"
        if message.is_topic_message:
            url += f'?topic={message.reply_to_message.message_thread_id}'
        chat_label = hlink(message.chat.title, url)
    else:
        chat_label = quote_html(repr(message.chat.title))

    text = "[ALERT] User {user} is reported message in chat {chat}.".format(
        user=message.from_user.get_mention(),
        chat=chat_label,
    )

    admin_ids = config.tg_bot.admin_ids
    if admin_ids:
        with suppress(Unauthorized):
            for admin_id in admin_ids:
                await message.bot.send_message(admin_id, text)
                logger.info("Send alert message to admin {admin}".format(admin=admin_id))
                await asyncio.sleep(0.3)

    await message.reply_to_message.reply("Сообщение было отправлено администраторам")


def register_report_command(dp: Dispatcher):
    dp.register_message_handler(text_report_admins,
                                F.ilter(F.reply_to_message),
                                chat_type=chat_types(),
                                commands=['report'],
                                commands_prefix='!/',
                                state='*')
