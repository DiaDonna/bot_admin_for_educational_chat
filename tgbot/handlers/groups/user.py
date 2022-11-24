from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ReplyKeyboardRemove

from tgbot.keyboards.reply.for_private import main_keyboard
from tgbot.utils.decorators import logging_message


@logging_message
async def user_start(message: Message) -> None:
    """ Хендлер для команды start (префикс команды '/' или '!') """

    keyboard = ReplyKeyboardRemove()
    if message.chat.type == ChatType.PRIVATE:
        keyboard = main_keyboard()

    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=keyboard)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], commands_prefix='/!', state="*", )
