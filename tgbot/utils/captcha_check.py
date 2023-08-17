import asyncio

from aiogram.types import ChatPermissions, CallbackQuery
from datetime import timedelta
from tgbot.utils.log_config import logger
from tgbot.config import user_dict, captcha_flag_user_dict, Config


async def check_captcha(call: CallbackQuery, config: Config):
    """
        func check pass rise ban or mute
               param call: CallbackQuery
               return None
        """
    password: str = call.data.split(':')[1]
    user_id: str = call.from_user.id
    chat_id: str = call.message.chat.id
    captcha_flag_user_dict.update({user_id: False})
    TIME_RISE_ASYNCIO: int = config.t_delta.time_rise_asyncio_ban
    TIME_MINUTE: int = config.t_delta.minute_delta
    if password.isdigit():
        if int(password) == user_dict.get(user_id):
            await call.answer(text=f"{call.from_user.full_name}"
                                   f" you are pass!", show_alert=True)
            captcha_flag_user_dict.update({user_id: True})
        else:
            await call.answer(text="don't be jerk!\n"
                                   "sit in the corner 4 min", show_alert=True)
            await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=int(user_id),
                                                        permissions=ChatPermissions(can_send_messages=False),
                                                        until_date=timedelta(seconds=TIME_MINUTE * 4))
            logger.info(f"User {user_id} was mute seconds = {TIME_MINUTE * 4}")
    else:
        await call.answer(text="wrong answer!\n"
                               "sit in the corner 1 min", show_alert=True)
        await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=int(user_id),
                                                    permissions=ChatPermissions(can_send_messages=False),
                                                    until_date=timedelta(seconds=TIME_MINUTE))
        logger.info(f"User {user_id} was mute seconds = {TIME_MINUTE}")

    # TODO change to schedule (use crone, scheduler, nats..)
    await asyncio.sleep(TIME_RISE_ASYNCIO)
    if captcha_flag_user_dict.get(user_id):
        captcha_flag_user_dict.pop(user_id)
        user_dict.pop(user_id)
    else:
        await call.message.bot.ban_chat_member(chat_id=chat_id, user_id=int(user_id),
                                               until_date=timedelta(seconds=TIME_MINUTE * 4))
        logger.info(f"User {user_id} was baned = {TIME_MINUTE * 4}")
