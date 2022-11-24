from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest

from tgbot.utils.chat_t import chat_types
from tgbot.utils.decorators import admin_and_bot_check
from tgbot.utils.log_config import logger
from tgbot.utils.update_log import add_to_log_message


async def ban(message: Message) -> None:
    """
    Хендлер для команды !b или !ban для роли ADMIN.
    Команда позволяет банить пользователя с описанием причины.
    Команду необходимо писать в ответе пересылаемого сообщения от того пользователя, которого нужно забанить.

    Handler for commands !b or !ban only for ADMIN.
    Command can be used for ban users with description of the reasons.
    You should write this command in response to a message from the user you want to ban.
    """
    await add_to_log_message(message=message)
    reason_for_ban: str = " ".join(message.text.split()[1:])

    try:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        logger.info("User {user} baned by {admin}".format(
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id)
        )
        await message.reply_to_message.answer(text=f'Пользователь {message.reply_to_message.from_user.get_mention()} '
                                                   f'<b>забанен</b> по причине: {reason_for_ban}')

    except BadRequest as e:
        logger.error("Failed to ban chat member: {error!r}", exc_info=e)
        await message.reply_to_message.answer(text=f'{message.from_user.get_mention()}, '
                                                   f'при выполнении команды возникла ошибка. Попробуйте еще раз.')


def register_bun(dp: Dispatcher) -> None:
    dp.register_message_handler(admin_and_bot_check(ban),
                                is_reply=True,
                                chat_type=chat_types(),
                                commands=["b", "ban"],
                                commands_prefix='!',
                                state="*",
                                is_admin=True)
