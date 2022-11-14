from aiogram import Dispatcher
from aiogram.types import Message


async def ban_to_user(message: Message) -> None:
    """
    Хендлер для команды !b для роли ADMIN

    Команда позволяет банить пользователя с описанием причины.
    Команду необходимо писать в ответе пересылаемого сообщения от того пользователя, которого нужно забанить.
    В противном случае админу отправляется сообщение с просьбой ввести команду корректно.
    """

    reason_for_ban: str = message.text[3:]  # причина бана, описанная админом в команде

    try:
        await message.bot.send_message(chat_id=message.chat.id,
                                       text=f'Пользователь {message.reply_to_message.from_user.id} '
                                            f'забанен по причине: {reason_for_ban}')
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)

    except AttributeError:
        await message.delete()
        await message.answer('Введите команду <i>!b</i> <b>в ответе на сообщение</b> от того пользователя, '
                             'которого хотите <i>забанить</i>')


def register_bun_to_user(dp: Dispatcher) -> None:
    dp.register_message_handler(ban_to_user, commands=["b"], commands_prefix='!', state="*", is_admin=True)
