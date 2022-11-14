from aiogram import Dispatcher
from aiogram.types import Message

from datetime import datetime, timedelta
from typing import List


async def set_readonly_to_user(message: Message) -> None:
    """
    Хендлер для команды !ro для роли ADMIN (с обязательными аргументами)

    Команда позволяет переводить пользователя в режим 'только чтение'.
    Команду необходимо писать в ответе пересылаемого сообщения от того пользователя, которого нужно перевести в этот
    режим.

        Обязательные аргументы команды:
        число - количество времени;
        буква(m - минуты, h - часы, d - дни, w - недели) - буквенное обозначение периода,
        на которое нужно перевести пользователя в режим 'только чтение'.

    В случаях если админ ввел команду без аргументов ИЛИ указал только 1 аргумент из двух обязательных ИЛИ указал
    неверные аргументы, то ему отправляется сообщение с просьбой ввести команду корректно.
    """

    args_list: List[str] = list(message.text[4:].strip())  # формируем список аргументов команды !ro
    time_delta: timedelta = timedelta(minutes=1)  # объявление переменной по умолчанию

    # если у команды 2 аргумента и оба удовлетворяют условию, то формируем правильную timedelta для параметра until_date
    if len(args_list) == 2 and (args_list[0].isdigit() and args_list[1] in ('h', 'd', 'w', 'm')):

        if args_list[1] == 'm':
            time_delta = timedelta(minutes=int(args_list[0]))
        elif args_list[1] == 'h':
            time_delta = timedelta(hours=int(args_list[0]))
        elif args_list[1] == 'd':
            time_delta = timedelta(days=int(args_list[0]))
        elif args_list[1] == 'w':
            time_delta = timedelta(weeks=int(args_list[0]))

        # обработка исключения на случай, если команда прописана не в пересылаемом сообщении
        try:
            await message.bot.restrict_chat_member(chat_id=message.chat.id,
                                                   user_id=message.reply_to_message.from_user.id,
                                                   until_date=datetime.now() + time_delta)
            await message.answer(f'Режим readonly включен для пользователя {message.reply_to_message.from_user.id} '
                                 f'на {"".join(args_list)}')

        except AttributeError:
            await message.delete()
            await message.answer('Введите команду <i>!ro</i> <b>в ответе на сообщение</b> от того пользователя, '
                                 'которому хотите установить режим <i>readonly</i>')

    # иначе если аргументы не переданы или переданы неверно
    else:
        await message.delete()
        await message.answer('Неверно указаны аргументы команды <i>!ro</i>')


def register_set_readonly_to_user(dp: Dispatcher) -> None:
    dp.register_message_handler(set_readonly_to_user, commands=["ro"], commands_prefix='!', state="*", is_admin=True)
