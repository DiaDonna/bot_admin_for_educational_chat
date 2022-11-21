import asyncio
from contextlib import suppress

from magic_filter import F

from aiogram import types, Dispatcher, Bot
from aiogram.utils.exceptions import Unauthorized
from aiogram.utils.markdown import hlink

from tgbot.config import Config
from tgbot.utils.admin_ids import get_admins_ids_for_report
from tgbot.utils.chat_t import chat_types
from tgbot.utils.log_config import logger


async def text_report_admins(message: types.Message, config: Config):
    """
    Хендлер для команды !report или /report.
    Позволяет пользователям пожаловаться на сообщение в чате.
    Следует писать только в ответ на сообщение, о котором необходимо сообщить.

    Handler for commands !report and /report.
    Command can be used for reporting to admins.
    You should write this command in response to a message you to report.
    """

    logger.info(
        "User {user} report message {message} in chat {chat} from user {from_user}".format(
            user=message.from_user.id,
            message=message.message_id,
            chat=message.chat.id,
            from_user=message.reply_to_message.from_user.id,
        ))

    # если группа частная, то формируем ссылку для перехода к группе,
    # а если публичная, то к ссылке на группу добавляем ссылку на сообщение для перехода к конкретному сообщению
    url_to_alert: str = await message.chat.get_url()
    if message.chat.username:
        url_to_alert: str = '/'.join([url_to_alert, f'{message.reply_to_message.message_id}'])

    chat_label: str = hlink(message.chat.title, url_to_alert)

    text = "[ALERT] Пользователь {user} пожаловался на сообщение в чате {chat}.".format(
        user=message.from_user.get_mention(),
        chat=chat_label,
    )

    admin_ids: list[int] = await get_admins_ids_for_report(message=message, config=config)

    for admin_id in admin_ids:
        with suppress(Unauthorized):
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
