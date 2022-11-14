from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation


async def help_command(message: Message) -> None:
    """
        Хендлер для команды !help

        Команда позволяет высылать список полезных ссылок пользователю в диалог с ботом.
        Команду можно писать как в группе, так и в ЛС боту от любой роли.

        В случаях если диалог с ботом не был инициализирован пользователем или бот был приостановлен, то пользователю
        высылается соответствующее сообщение.
        """

    # текст для пользователя с полезными ссылками
    # test = await message.bot.get_my_default_administrator_rights()
    helping_text: str = \
        (f'Привет, {message.from_user.first_name}!'
         
         f'\n\nСсылка на <b>базовые советы по дипломному проекту:</b>'
         f'<a href="https://magnetic-evergreen-187.notion.site/Python-Basic-3ac614e60b7e434e9d9c018023319c04"> ТУТ </a>'
         
         f'\n\nСсылка на <b>видео по подключению к базам данных:</b>'
         f'<a href="https://youtu.be/TCdyfEvrIUg?list=PLA0M1Bcd0w8x4Inr5oYttMK6J47vxgv6J"> перейти в youtube </a>'
         
         f'\n\nP.S. Итоговая презентация проектов - отменена. '
         f'Вместо неё только защита дипломного проекта перед куратором.\n'
         f'Вы можете посмотреть записи прошедших презентаций по'
         f'<a href="https://docs.google.com/spreadsheets/d/1KbM7aPC4iYcNqm89nUNlQkplxQdfFGYdT2whYgF4V38/edit#gid=0">'
         f' ссылке </a>')

    # обработка исключений на случаи, если диалог с ботом не был инициализирован или был приостановлен пользователем
    try:
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text=helping_text,
                                       disable_web_page_preview=True)
        await message.delete()

    except BotBlocked:
        await message.reply(f'Я не могу написать вам, т.к. вы приостановили диалог со мной.\n'
                            f'Возобновите диалог и попробуйте снова:\n'
                            f'@EducationalChatAdmin_bot')
    except CantInitiateConversation:
        await message.reply(f'Я не могу написать вам, т.к. вы не инициализировали диалог со мной.\n'
                            f'Отправьте команду <i>/start</i> мне в ЛС:\n'
                            f'@EducationalChatAdmin_bot')


def register_help_command(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=['help'], commands_prefix='!/', state="*")
