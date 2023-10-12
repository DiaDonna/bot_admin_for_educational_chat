import asyncio

from aiogram.types import ChatPermissions, CallbackQuery, Message, ReplyKeyboardRemove, User
from datetime import timedelta

from typing import List

from tgbot.utils.texts import greeting_text
from tgbot.utils.log_config import logger
from tgbot.utils.admin_ids import get_admins_ids_for_help_and_paste
from tgbot.config import user_dict, capcha_flag_user_dict, Config


async def check_captcha(call: CallbackQuery, config: Config):
    """
        func check pass rise ban or mute
               param call: CallbackQuery
               return None
        """
    # TODO 1) new bag aiogram.utils.exceptions.MethodIsNotAvailable: Method is available only for supergroups
    # TODO    is bag if group not super , add handler admin, type group
    # FIXME 2) optimise ternary
    # FIXME 3) no check if admin
    admin_ids: List[int] = await get_admins_ids_for_help_and_paste(call.message)
    password: int = int(call.data.split(':')[1])
    user_id: int = int(call.from_user.id)
    chat_id: int = int(call.message.chat.id)
    minute_delta: int = config.time_delta.minute_delta
    if user_id in admin_ids:
        msg_temp = await call.message.answer(text="Админ не балуйся \n"
                                                  "иди работать!")
        await asyncio.sleep(minute_delta)
        try:
            await msg_temp.delete()
        except AttributeError as error:
            logger.info(f"user id {user_id}  {error}")

        logger.info(f"admin:{user_id} name:{call.from_user.full_name} was play")
    else:
        if user_id in user_dict.keys():
            capcha_flag_user_dict.update({user_id: False})
            if password == user_dict.get(user_id):
                await call.answer(text=f"{call.from_user.full_name}"
                                       f" you are pass!", show_alert=True)
                await call.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                                    permissions=ChatPermissions(can_send_messages=True),
                                                    until_date=timedelta(seconds=minute_delta))
                await call.bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
                logger.info(f"User id:{user_id} name:{call.from_user.full_name}was pass")
                capcha_flag_user_dict.update({user_id: True})
                bot_user: User = await call.message.bot.get_me()
                greeting: str = greeting_text(call=call, bot_user=bot_user)
                msg: Message = await call.message.answer(text=greeting, disable_web_page_preview=True,
                                                         reply_markup=ReplyKeyboardRemove())
                logger.info(f"New User id:{user_id} name:{call.from_user.full_name} was greeting")
                await asyncio.sleep(config.time_delta.time_rise_asyncio_del_msg)
                await msg.delete()
                logger.info(f"del greeting msg for {user_id}")

            else:
                await call.answer(text="wrong answer!\n"
                                       "sit in the corner 1 min", show_alert=True)
                await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                                            permissions=ChatPermissions(can_send_messages=False),
                                                            until_date=timedelta(seconds=minute_delta))
                logger.info(f"User id:{user_id} name:{call.from_user.full_name} was mute seconds = {minute_delta}")

        else:
            await call.answer(text="don't be jerk!\n"
                                   "sit in the corner 4 min", show_alert=True)
            await call.message.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                                        permissions=ChatPermissions(can_send_messages=False),
                                                        until_date=timedelta(seconds=minute_delta * 4))
            logger.info(f"User id:{user_id} name:{call.from_user.full_name} was mute seconds = {minute_delta * 4}")