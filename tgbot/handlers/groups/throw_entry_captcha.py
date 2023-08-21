import random
import asyncio
from datetime import timedelta

from aiogram import Dispatcher
from aiogram.types import Message, InputFile

from tgbot.utils.captcha import gen_captcha
from tgbot.keyboards.Inline.captcha_keys import gen_captcha_button_builder
from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.config import user_dict, Config, captcha_flag_user_dict


@logging_message
async def handler_throw_captcha(message: Message, config: Config) -> None:
    """Handler for generate captcha image to user
           param message: Message
           return None
    """
    password: int = random.randint(1000, 9999)
    user_id: str = message.from_user.id
    user_name: str = message.from_user.full_name
    captcha_image: InputFile = InputFile(gen_captcha(password))
    user_dict.update({user_id: password})
    chat_id: str = message.chat.id
    time_rise_asyncio_ban: int = config.time_delta.time_rise_asyncio_ban
    minute_delta: int = config.time_delta.minute_delta
    time_rise_asyncio_del_msg = config.time_delta.time_rise_asyncio_del_msg
    msg = await message.answer_photo(photo=captcha_image, caption=f'for{user_name}'
                                                                  f' this {password} is answer',
                                     reply_markup=gen_captcha_button_builder(password)
                                     )

    # TODO change to schedule (use crone, scheduler, nats..)
    await asyncio.sleep(time_rise_asyncio_ban)
    if captcha_flag_user_dict.get(user_id):
        captcha_flag_user_dict.pop(user_id)
        user_dict.pop(user_id)
    else:
        await message.bot.ban_chat_member(chat_id=chat_id, user_id=int(user_id),
                                          until_date=timedelta(seconds=minute_delta * 4))
        logger.info(f"User {user_id} was baned = {minute_delta * 4}")
    await asyncio.sleep(time_rise_asyncio_del_msg)
    await msg.delete()

    logger.info(f"User {user_id} throw captcha")


def register_captcha(dp: Dispatcher) -> None:
    dp.register_message_handler(handler_throw_captcha,
                                commands=['captcha'],
                                commands_prefix='!/',
                                state="*")
