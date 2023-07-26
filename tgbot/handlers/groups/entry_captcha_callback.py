from aiogram import Dispatcher
from aiogram.types import CallbackQuery
user_dict: dict = dict()


async def captcha_answer(call: CallbackQuery) -> None:
    """handler for inline captcha answer button
           param call: CallbackQuery
           return None
    """
    password: str = call.data.split(':')[1]
    user_id: str = call.from_user.id
    if password.isdigit():
        if int(password) == user_dict.get(user_id):
            await call.answer(text=f"{call.from_user.full_name} you are pass!", show_alert=True)
        else:
            await call.answer(text="don't be jerk!", show_alert=True)
    else:
        await call.answer(text="no you are block!", show_alert=True)


def register_callback_captcha(dp: Dispatcher):
    dp.register_callback_query_handler(captcha_answer, lambda call: call.data.startswith("answer_button"))
