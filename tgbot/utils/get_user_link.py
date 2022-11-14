from aiogram import md
from aiogram import types
from aiogram.utils.markdown import quote_html


async def get_link(user: types.User) -> str:
    """
    Возвращает ссылку с пользователем для вывода сообщения
    :param user: types.User
    :return: str
    """
    if not user.url:
        return 'пользователь'
    if user.first_name:
        username = user.first_name
        if user.last_name:
            username += f' {user.last_name}'
    elif user.username:
        username = quote_html(user.username)
    else:
        username = 'пользователь'
    return md.hlink(username, user.url)
