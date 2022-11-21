from aiogram import Dispatcher
from aiogram.types import ChatType, Message


async def echo_for_private(message: Message):
    """ Эхо-хендлер для ЛС с ботом. На команды высылает инфо-сообщение о недоступности использования команд в ЛС.
    На остальные сообщения (в том числе пересылаемые) и отсылаемые медиа никак не реагирует. """

    await message.reply('Все мои команды доступны только для групп')


def register_echo(dp: Dispatcher):

    dp.register_message_handler(echo_for_private,
                                chat_type=ChatType.PRIVATE,
                                commands=['help', 'report', 'paste'],
                                state='*')
