import asyncio

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ChatPermissions
from datetime import timedelta
from tgbot.utils.log_config import logger
from tgbot.utils.decorators import logging_message
from tgbot.config import user_dict, captcha_flag
# TODO add mute before captcha answer, remove bag(BAN IF ANSWER TO ANOTHER CAPTCHA).


@logging_message
async def captcha_answer(call: CallbackQuery) -> None:
    """handler for inline captcha answer button
           param call: CallbackQuery
           return None
    """
    password: str = call.data.split(':')[1]
    user_id: str = call.from_user.id
    chat_id: str = call.message.chat.id
    captcha_flag.update({user_id: False})
    if password.isdigit():
        if int(password) == user_dict.get(user_id):
            await call.answer(text=f"{call.from_user.full_name}"
                                   f" you are pass!", show_alert=True)
            captcha_flag.update({user_id: True})
        else:
            await call.answer(text="don't be jerk!\n"
                                   "sit in the corner 4 min", show_alert=True)
            await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=int(user_id),
                                                        permissions=ChatPermissions(can_send_messages=False),
                                                        until_date=timedelta(seconds=240))
            logger.info(f"User {user_id} was mute seconds = {240}")
    else:
        await call.answer(text="wrong answer!\n"
                               "sit in the corner 1 min", show_alert=True)
        await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=int(user_id),
                                                    permissions=ChatPermissions(can_send_messages=False),
                                                    until_date=timedelta(seconds=60))
        logger.info(f"User {user_id} was mute seconds = {240}")
    # TODO change to schedule (use crone, scheduler, nats..)
    await asyncio.sleep(1800)
    if captcha_flag:
        captcha_flag.pop(user_id)
        user_dict.pop(user_id)
    else:
        await call.message.bot.ban_chat_member(chat_id=chat_id, user_id=int(user_id),
                                               until_date=timedelta(seconds=240))
        logger.info(f"User {user_id} was baned = {240}")


def register_callback_captcha(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(captcha_answer,
                                       lambda call: call.data.startswith("answer_button"))
