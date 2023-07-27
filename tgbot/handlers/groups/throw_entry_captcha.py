import random
import asyncio

from aiogram import Dispatcher
from aiogram.types import Message, InputFile

from tgbot.utils.captcha import throw_captcha
from tgbot.keyboards.Inline.captcha_keys import gen_captcha_button_builder
from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.config import user_dict


@logging_message
async def captcha(message: Message) -> None:
    """handler for generate captcha image too user
           param message: Message
           return None
    """
    password: int = random.randint(1000, 9999)
    user: str = message.from_user.id
    user_id: str = message.new_chat_members[0].id
    user_name: str = message.from_user.full_name
    captcha_image: InputFile = InputFile(throw_captcha(password))
    user_dict.update({user: password})

    msg = await message.answer_photo(photo=captcha_image, caption=f'for{user_name}'
                                                                  f' this {password} is answer',
                                     reply_markup=gen_captcha_button_builder(password)
                                     )
    await asyncio.sleep(300)
    await msg.delete()

    logger.info(f"User {user_id} throw captcha")


def register_captcha(dp: Dispatcher) -> None:
    dp.register_message_handler(captcha,
                                commands=['captcha'],
                                commands_prefix='/!',
                                state="*")
