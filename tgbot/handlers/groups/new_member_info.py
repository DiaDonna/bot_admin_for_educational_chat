import random
import asyncio

from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove, CallbackQuery, InputFile

from tgbot.utils.decorators import logging_message
from tgbot.utils.log_config import logger
from tgbot.utils.texts import greeting_text
from tgbot.utils.captcha import throw_captcha
from tgbot.keyboards.Inline.captcha_keys import gen_captcha_button_builder

user_dict: dict = dict()


@logging_message
async def new_member_info(message: Message) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """

    bot_user = await message.bot.get_me()
    greeting: str = greeting_text(message=message, bot_user=bot_user)
    password: int = random.randint(1000, 9999)
    user: str = await message.from_user.id
    captcha: InputFile = InputFile(throw_captcha(password))
    user_dict.update({user: password})

    await message.answer(text=greeting, disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
    logger.info("New User {user} was greeting".format(
        user=message.new_chat_members[0].id)
    )
    msg = await message.answer_photo(photo=captcha, caption=f'for{message.from_user.full_name}'
                                                            f' this {password} is answer',
                                     reply_markup=gen_captcha_button_builder(password)
                                     )
    await asyncio.sleep(30)
    await msg.delete()


def register_new_member_info(dp: Dispatcher):
    dp.register_message_handler(new_member_info,
                                content_types=ContentTypes.NEW_CHAT_MEMBERS)
