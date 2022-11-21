from aiogram import Dispatcher
from aiogram.types import ChatType, Message


async def echo_for_private(message: Message):
    """ Эхо-хендлер для ЛС с ботом """

    await message.answer('Все мои команды доступны только для группы.')


def register_echo(dp: Dispatcher):

    dp.register_message_handler(echo_for_private,
                                chat_type=ChatType.PRIVATE,
                                state='*')
