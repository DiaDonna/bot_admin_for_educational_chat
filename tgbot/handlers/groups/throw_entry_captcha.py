import random
import asyncio

from aiogram import Dispatcher
from aiogram.types import Message, InputFile

from tgbot.utils.captcha import gen_captcha
from tgbot.keyboards.Inline.captcha_keys import gen_captcha_button_builder
from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.config import user_dict


@logging_message
async def handler_throw_captcha(message: Message) -> None:
    """Handler for generate captcha image to user
           param message: Message
           return None
    """
    password: int = random.randint(1000, 9999)
    user: str = message.from_user.id
    user_id: str = message.new_chat_members[0].id
    user_name: str = message.from_user.full_name
    captcha_image: InputFile = InputFile(gen_captcha(password))
    user_dict.update({user: password})
    time_rise_asyncio = 300

    msg = await message.answer_photo(photo=captcha_image, caption=f'for{user_name}'
                                                                  f' this {password} is answer',
                                     reply_markup=gen_captcha_button_builder(password)
                                     )
    await asyncio.sleep(time_rise_asyncio)
    await msg.delete()

    logger.info(f"User {user_id} throw captcha")


def register_captcha(dp: Dispatcher) -> None:
    dp.register_message_handler(handler_throw_captcha,
                                commands=['captcha'],
                                commands_prefix='/!',
                                state="*")
