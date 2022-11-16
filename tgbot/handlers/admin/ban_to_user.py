import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest, MessageCantBeDeleted
from magic_filter import F

from tgbot.utils.chat_t import chat_types


async def ban(message: Message) -> None:
    """
    Хендлер для команды !b для роли ADMIN

    Команда позволяет банить пользователя с описанием причины.
    Команду необходимо писать в ответе пересылаемого сообщения от того пользователя, которого нужно забанить.

    Handler for commands !b, !ban, only for ADMIN

    Command can be used for ban users with description of the reasons.
    You should write this command in response to a message from the user you want to ban.
    """

    logger = logging.getLogger(__name__)

    reason_for_ban: str = " ".join(message.text.split()[1:])

    try:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        logger.info("User {user} baned by {admin}".format(
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id))
        await message.reply_to_message.answer(text=f'Пользователь {message.reply_to_message.from_user.get_mention()} '
                                                   f'<b>забанен</b> по причине: {reason_for_ban}')
    except BadRequest as e:
        logger.error("Failed to ban chat member: {error!r}", exc_info=e)


def register_bun(dp: Dispatcher) -> None:
    dp.register_message_handler(ban,
                                F.ilter(F.reply_to_message),
                                chat_type=chat_types(),
                                bot_can_restrict=True,
                                commands=["b", "ban"],
                                commands_prefix='!',
                                state="*",
                                is_admin=True)
