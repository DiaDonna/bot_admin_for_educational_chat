from aiogram import Dispatcher
from aiogram.types import Message


async def user_start(message: Message) -> None:
    """ Хендлер для команды start (префикс команды '/' или '!') """

    await message.answer(f'Привет, {message.from_user.first_name}!')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], commands_prefix='/!', state="*")

