from typing import List

from aiogram.types import Message

from tgbot.utils.texts import admin_help_text, user_help_text


async def choice_for_helping_text(message: Message, admins: List[int]) -> str:
    """ Функция для корректировки отправляемого текста на команду help в зависимости от роли (юзер/админ)

    :param message: объект сообщения от пользователя;
    :param admins: список ID администраторов, указанных в переменной окружения

    :return: текст для команды help
    """

    in_admins: bool = message.from_user.id in admins

    if in_admins:
        help_text = get_admin_text(message)

    else:
        help_text = get_user_text(message)

    return help_text


def get_admin_text(message: Message) -> str:

    helping_text: str = admin_help_text(message=message)
    return helping_text


def get_user_text(message: Message) -> str:

    helping_text: str = user_help_text(message=message)
    return helping_text

