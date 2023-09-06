import asyncio

from aiogram.types import ChatPermissions, CallbackQuery, Message, ReplyKeyboardRemove, User
from datetime import timedelta
from tgbot.utils.texts import greeting_text
from tgbot.utils.log_config import logger
from tgbot.config import user_dict, captcha_flag_user_dict, Config


async def check_captcha(call: CallbackQuery, config: Config):
    """
        func check pass rise ban or mute
               param call: CallbackQuery
               return None
        """
    # TODO 1) new bag aiogram.utils.exceptions.MethodIsNotAvailable: Method is available only for supergroups
    # TODO    is bag if group not super , add handler admin, type group
    # TODO 2) optimise ternary
    password: str = call.data.split(':')[1]
    user_id: int = int(call.from_user.id)
    chat_id: int = int(call.message.chat.id)
    captcha_flag_user_dict.update({user_id: False})
    minute_delta: int = config.time_delta.minute_delta
    if password.isdigit():
        if int(password) == user_dict.get(user_id):
            await call.answer(text=f"{call.from_user.full_name}"
                                   f" you are pass!", show_alert=True)
            await call.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                                permissions=ChatPermissions(can_send_messages=True),
                                                until_date=timedelta(seconds=minute_delta))
            logger.info(f"User id:{user_id} name:{call.from_user.full_name}was pass")
            captcha_flag_user_dict.update({user_id: True})
            bot_user: User = await call.message.bot.get_me()
            greeting: str = greeting_text(call=call, bot_user=bot_user)
            msg: Message = await call.message.answer(text=greeting, disable_web_page_preview=True,
                                                     reply_markup=ReplyKeyboardRemove())
            logger.info(f"New User id:{user_id} name:{call.from_user.full_name} was greeting")
            await asyncio.sleep(config.time_delta.time_rise_asyncio_del_msg)
            await msg.delete()

        else:
            await call.answer(text="don't be jerk!\n"
                                   "sit in the corner 4 min", show_alert=True)
            await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                                        permissions=ChatPermissions(can_send_messages=False),
                                                        until_date=timedelta(seconds=minute_delta * 4))
            captcha_flag_user_dict.update({user_id: True})
            logger.debug(f"User id:{user_id} name:{call.from_user.full_name} was mute seconds = {minute_delta * 4}")
    else:
        await call.answer(text="wrong answer!\n"
                               "sit in the corner 1 min", show_alert=True)
        await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                                    permissions=ChatPermissions(can_send_messages=False),
                                                    until_date=timedelta(seconds=minute_delta))
        logger.debug(f"User id:{user_id} name:{call.from_user.full_name} was mute seconds = {minute_delta}")
