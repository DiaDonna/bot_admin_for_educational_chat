from aiogram import Dispatcher, types
from aiogram.types import Message

from tgbot.utils.log_config import logger


async def new_member_info(message: Message) -> None:
    """
    Хендлер для приветствия нового пользователя группы с полезными ссылками.

    Handler for greeting new user in group and sending to him some useful links
    """

    bot_user = await message.bot.get_me()

    greeting: str = (f'Привет, {message.new_chat_members[0].get_mention()}!\n\n'
                     f'Прежде чем задавать вопросы - прочитай <b>базовые советы по дипломному проекту:</b> '
                     f'<a href="https://magnetic-evergreen-187.notion.site/Python-Basic'
                     f'-3ac614e60b7e434e9d9c018023319c04"> ТУТ </a> '
                     f'\n\nА также ознакомься со всеми <b>закрепленными сообщениями</b> в этом чате.\n\n'
                     f'Чтобы получить доступ к командам в этой группе - '
                     f'напиши мне в ЛС @{bot_user.username} команду <i>/start</i>')

    await message.answer(text=greeting, disable_web_page_preview=True)
    logger.info("New User {user} was greeting".format(
        user=message.new_chat_members[0].id)
    )


def register_new_member_info(dp: Dispatcher):
    dp.register_message_handler(new_member_info,
                                content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
