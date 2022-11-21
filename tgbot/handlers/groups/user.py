from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.reply.for_private import main_keyboard


async def user_start(message: Message) -> None:
    """ Хендлер для команды start (префикс команды '/' или '!') """

    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=main_keyboard())


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], commands_prefix='/!', state="*")

