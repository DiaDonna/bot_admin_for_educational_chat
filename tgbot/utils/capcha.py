from io import BytesIO
from captcha.image import ImageCaptcha

import random
import asyncio
from datetime import timedelta

from aiogram.types import Message, InputFile, ChatPermissions, ChatMemberUpdated, ReplyKeyboardRemove, ChatMember
from typing import List

from tgbot.keyboards.Inline.captcha_keys import gen_captcha_button_builder
from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.config import user_dict, Config, capcha_flag_user_dict


async def dict_pop_executor(user_id: int) -> None:
    """
    Take id int, execute pop in dicts
    param user_id: int
    return: None
    """
    try:
        capcha_flag_user_dict.pop(user_id, None)
        user_dict.pop(user_id, None)
        logger.info(f"pop_execute  {user_id} del")
    except KeyError as error:
        logger.info(f"{error} error by key {user_id}")


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
async def throw_capcha(message: ChatMemberUpdated, config: Config) -> None:
    """
           generate captcha image send to user in chat
           param message: Message
           return None
    """
    admins: List[ChatMember] = await message.bot.get_chat_administrators(message.chat.id)
    admin_ids: List[int] = [admin.user.id for admin in admins if not admin.user.is_bot]
    user_id: int = int(message.from_user.id)
    user_name: str = message.from_user.full_name
    chat_id: int = int(message.chat.id)
    time_rise_asyncio_ban: int = config.time_delta.time_rise_asyncio_ban
    minute_delta: int = config.time_delta.minute_delta
    try:
        new_user_id: int = int(message.new_chat_member.user.id)
        user_id = new_user_id
        user_name = message.new_chat_member.user.full_name
    except IndexError as err:
        logger.info(f"User {user_id} {user_name} not new {err}")
    if user_id in admin_ids:
        msg = await message.bot.send_message(chat_id=chat_id, disable_web_page_preview=True,
                                             text="Админ не балуйся иди работать!", reply_markup=ReplyKeyboardRemove())
        logger.info("New User {user} was greeting".format(
            user=message.new_chat_member.user.id)
        )
        await asyncio.sleep(minute_delta)
        await msg.delete()
        logger.info(f"admin:{user_id} name:{message.from_user.full_name} was play")
    else:
        password: int = random.randint(1000, 9999)
        user_dict.update({user_id: password})
        captcha_image: InputFile = InputFile(gen_captcha(password))
        await message.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                               permissions=ChatPermissions(can_send_messages=False),
                                               until_date=timedelta(seconds=time_rise_asyncio_ban))
        logger.info(f"User {user_id} mute before answer")
        caption: str = f'Привет, {user_name} пожалуйста ответьте {password} иначе Вас кикнут!'
        msg: Message = await message.bot.send_photo(chat_id=chat_id,
                                                    photo=captcha_image,
                                                    caption=caption,
                                                    reply_markup=gen_captcha_button_builder(password)
                                                    )
        logger.info(f"User {user_id} throw captcha")
        # FIXME change to schedule (use crone, scheduler, nats..)
        await asyncio.sleep(time_rise_asyncio_ban)
        await msg.delete()
        if capcha_flag_user_dict.get(user_id):
            await dict_pop_executor(user_id)
        else:
            await message.bot.kick_chat_member(chat_id=chat_id, user_id=user_id,
                                               until_date=timedelta(seconds=minute_delta))
            logger.info(f"User {user_id} was kicked = {minute_delta}")
            await dict_pop_executor(user_id)
        logger.info(f"for User {user_id} del msg captcha")


if __name__ == '__main__':
    pass
