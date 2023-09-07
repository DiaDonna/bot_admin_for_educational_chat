from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from typing import List


def gen_captcha_keys(temp: int) -> List[InlineKeyboardButton]:
    """
     Take answer, generate object buttons, return list of object: "KeyboardButton"
    param temp: int answer of the captcha
    return: list of "KeyboardButton" with answer
    """
    temp_str: str = str(temp)
    numbers_wrong_button: int = 3
    first_button: InlineKeyboardButton = InlineKeyboardButton(
        text=temp_str, callback_data=f"answer_button:{temp_str}")
    wrong_button: InlineKeyboardButton = InlineKeyboardButton(
        text='wrong_answer', callback_data="answer_button:joke")

    out_list = [first_button, *[wrong_button for _ in range(numbers_wrong_button)]]
    random.shuffle(out_list)
    return out_list


def gen_captcha_button_builder(temp: int) -> InlineKeyboardMarkup:
    """trow int, add buttons, return object:"ReplyKeyboardMarkup"
       param temp: int answer of the captcha
       return object:ReplyKeyboardMarkup"""
    captcha_builder: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    captcha_buttons: list = gen_captcha_keys(temp)
    for i in range(len(captcha_buttons)):
        captcha_builder.add(captcha_buttons[i])
    keyboard_captcha: InlineKeyboardMarkup = captcha_builder
    return keyboard_captcha


if __name__ == '__main__':
    pass
