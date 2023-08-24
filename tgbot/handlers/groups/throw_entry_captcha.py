import random
import asyncio
from datetime import timedelta

from aiogram import Dispatcher
from aiogram.types import Message, InputFile, ChatPermissions

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
    user_id: int = int(message.from_user.id)
    user_name: str = message.from_user.full_name
    captcha_image: InputFile = InputFile(gen_captcha(password))
    chat_id: int = int(message.chat.id)
    time_rise_asyncio_ban: int = config.time_delta.time_rise_asyncio_ban
    minute_delta: int = config.time_delta.minute_delta
    time_rise_asyncio_del_msg = config.time_delta.time_rise_asyncio_del_msg
    new_user_id: int = int(message.new_chat_members[0].id)
    if new_user_id is not user_id:
        user_id = new_user_id
        user_name = message.new_chat_members[0].get_mention()
    user_dict.update({user_id: password})
    await message.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                           permissions=ChatPermissions(can_send_messages=False),
                                           until_date=timedelta(seconds=minute_delta))
    logger.info(f"User {user_id} was mute before answer captcha")
    msg: Message = await message.answer_photo(photo=captcha_image, caption=f'for {user_name}'
                                                                           f' this {password} is answer',
                                              reply_markup=gen_captcha_button_builder(password)
                                              )
    logger.info(f"User {user_id} throw captcha")
    # TODO change to schedule (use crone, scheduler, nats..)
    await asyncio.sleep(time_rise_asyncio_ban)
    await msg.delete()
    new_user_id: int = int(*user_dict.keys())
    if new_user_id is not user_id:
        user_id = new_user_id
    if captcha_flag_user_dict.get(user_id):
        captcha_flag_user_dict.pop(user_id)
        user_dict.pop(user_id)
    else:
        await message.bot.kick_chat_member(chat_id=chat_id, user_id=user_id,
                                           until_date=timedelta(seconds=minute_delta))
        logger.info(f"User {user_id} was kicked = {minute_delta}")
        user_dict.pop(user_id)
    await asyncio.sleep(time_rise_asyncio_del_msg)
    logger.info(f"for User {user_id} del msg captcha")
    # TODO add log del msg


def register_captcha(dp: Dispatcher) -> None:
    dp.register_message_handler(handler_throw_captcha,
                                commands=['captcha'],
                                commands_prefix='!/',
                                state="*")
