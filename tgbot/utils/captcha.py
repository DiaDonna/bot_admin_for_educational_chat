from io import BytesIO
from captcha.image import ImageCaptcha

import random
import asyncio
from datetime import timedelta

from aiogram.types import Message, InputFile, ChatPermissions
from tgbot.keyboards.Inline.captcha_keys import gen_captcha_button_builder
from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.config import user_dict, Config, captcha_flag_user_dict


async def dict_pop_executor(user_id: int) -> None:
    """
    Take id int, execut pop in dicts
    param user_id: int
    return: None
    """
    try:
        captcha_flag_user_dict.pop(user_id, None)
        user_dict.pop(user_id, None)
        logger.info(f"pop_execut  {user_id} del\n")
    except Exception as error:
        logger.info(f"error by key {user_id}\n {error}")


def gen_captcha(temp_integer: int) -> BytesIO:
    """
     Take some int, generate object ImageCaptcha -> BytesIO return object BytesIO
    param temp_integer: int
    return: BytesIO
    """
    image: ImageCaptcha = ImageCaptcha()
    data: BytesIO = image.generate(str(temp_integer))
    return data


@logging_message
async def throw_captcha(message: Message, config: Config) -> None:
    """
           generate captcha image send to user in chat
           param message: Message
           return None
    """
    user_id: int = int(message.from_user.id)
    user_name: str = message.from_user.full_name
    chat_id: int = int(message.chat.id)
    time_rise_asyncio_ban: int = config.time_delta.time_rise_asyncio_ban
    minute_delta: int = config.time_delta.minute_delta
    new_user_id: int = int(message.new_chat_members[0].id)
    if new_user_id is not user_id:
        user_id = new_user_id
        user_name = message.new_chat_members[0].get_mention()

    password: int = random.randint(1000, 9999)
    user_dict.update({user_id: password})
    captcha_image: InputFile = InputFile(gen_captcha(password))
    await message.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                           permissions=ChatPermissions(can_send_messages=False),
                                           until_date=timedelta(seconds=minute_delta))
    logger.info(f"User {user_id} {message.new_chat_members[0]} mute before answer")
    msg: Message = await message.answer_photo(photo=captcha_image, caption=f'for {user_name}'
                                                                           f' this {password} is answer',
                                              reply_markup=gen_captcha_button_builder(password)
                                              )
    logger.info(f"User {user_id} throw captcha")
    # FIXME change to schedule (use crone, scheduler, nats..)
    await asyncio.sleep(time_rise_asyncio_ban)
    await msg.delete()
    if captcha_flag_user_dict.get(user_id):
        await dict_pop_executor(user_id)
    else:
        await message.bot.kick_chat_member(chat_id=chat_id, user_id=user_id,
                                           until_date=timedelta(seconds=minute_delta))
        logger.warning(f"User {user_id} was kicked = {minute_delta}")
        await dict_pop_executor(user_id)
    logger.info(f"for User {user_id} del msg captcha")


if __name__ == '__main__':
    pass
