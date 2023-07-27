import random
import asyncio

from aiogram import Dispatcher
from aiogram.types import Message, InputFile

from tgbot.utils.captcha import throw_captcha
from tgbot.keyboards.Inline.captcha_keys import gen_captcha_button_builder

user_dict: dict = dict()


async def captcha(message: Message) -> None:
    """handler for generate captcha image too user
           param message: Message
           return None
    """
    password: int = random.randint(1000, 9999)
    user: str = message.from_user.id
    captcha_image: InputFile = InputFile(throw_captcha(password))
    user_dict.update({user: password})
    msg = await message.answer_photo(photo=captcha_image, caption=f'for{message.from_user.full_name}'
                                                                  f' this {password} is answer',
                                     reply_markup=gen_captcha_button_builder(password)
                                     )
    await asyncio.sleep(300)
    await msg.delete()


def register_captcha(dp: Dispatcher):
    dp.register_message_handler(captcha,
                                commands=['captcha'],
                                commands_prefix='/!',
                                state="*")
