
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.utils.captcha import throw_captcha
from tgbot.utils.decorators import logging_message
from tgbot.config import Config


@logging_message
async def handler_throw_captcha(message: Message, config: Config) -> None:
    """Handler for generate captcha image to user
           param message: Message
           return None
    """
    await throw_captcha(message=message, config=config)


def register_captcha(dp: Dispatcher) -> None:
    dp.register_message_handler(handler_throw_captcha,
                                commands=['captcha'],
                                commands_prefix='!/',
                                state="*")
