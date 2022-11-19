from functools import wraps
from typing import Callable, Any

from aiogram.types import Message

from tgbot.filters.admin import AdminFilter


def admin_and_bot_check(func: Callable) -> Callable:
    """ Декоратор для хендлера, который не позволяет наложить ограничение (бан или "только чтение") на бота, владельца
    или администратора чата """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        message: Message = args[0]

        is_bot: bool = message.reply_to_message.from_user.is_bot
        is_admin: bool = await AdminFilter.check(message.reply_to_message)

        if not is_admin and not is_bot:
            return await func(*args, **kwargs)

        await message.reply_to_message.answer(text=f'{message.from_user.get_mention()}, '
                                                   f'вы не можете ограничить бота, владельца или администратора чата!')

    return wrapper
