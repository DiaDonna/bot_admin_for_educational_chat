import logging
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from aiogram.utils.exceptions import BadRequest, MessageCantBeDeleted
from magic_filter import F

from tgbot.utils.chat_t import chat_types
from tgbot.utils.get_user_link import get_link


async def ban_to_user(message: Message) -> None:
    """
    Хендлер для команды !b для роли ADMIN

    Команда позволяет банить пользователя с описанием причины.
    Команду необходимо писать в ответе пересылаемого сообщения от того пользователя, которого нужно забанить.
    В противном случае админу отправляется сообщение с просьбой ввести команду корректно.
    """

    logger = logging.getLogger(__name__)

    reason_for_ban: str = " ".join(message.text.split()[1:])

    try:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        logger.info("User {user} baned by {admin}".format(
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id))
        await message.reply_to_message.answer(text=f'Пользователь {message.reply_to_message.from_user.get_mention()} '
                                                   f'забанен по причине: {reason_for_ban}')
    except BadRequest as e:
        logger.error("Failed to ban chat member: {error!r}", exc_info=e)
        with suppress(MessageCantBeDeleted):
            await message.delete()


def register_bun_to_user(dp: Dispatcher) -> None:
    dp.register_message_handler(ban_to_user,
                                F.ilter(F.reply_to_message),
                                chat_type=chat_types(),
                                commands=["b", "ban"],
                                commands_prefix='!',
                                state="*",
                                is_admin=True)
