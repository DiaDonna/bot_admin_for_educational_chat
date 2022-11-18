from typing import List

from aiogram.types import Message

from tgbot.filters.admin import AdminFilter


async def choice_for_helping_text(message: Message, admins: List[int]) -> str:
    """ Функция для корректировки отправляемого текста на команду help в зависимости от роли (юзер/админ)

    :param message: объект сообщения от пользователя;
    :param admins: список ID администраторов, указанных в переменной окружения

    :return: текст для команды help
    """

    is_admin: bool = await AdminFilter.check(message=message)  # проверка на админа в чате
    in_admins: bool = message.from_user.id in admins  # проверка на наличие ID админа в переменной окружения

    if is_admin or in_admins:
        helping_text: str = \
            (f'Привет, администратор {message.from_user.get_mention()}!'

             f'\n\n<b>Список доступных команд:</b>'
             f'\n<i>Обе команды необходимо вводить в ответ на пересылаемое сообщение от пользователя, '
             f'к которому хотите применить команду.</i>'

             f'\n\n<b>!b или !ban</b> &lt;<i>причина бана</i>&gt; - Забанить пользователя c указанием причины. '
             f'\n<i>Всё, что будет написано через 1 пробел после команды - будет указано в инфо-сообщении</i>'

             f'\n\n<b>!ro</b> &lt;<i>число</i>&gt;&lt;<i>время</i>&gt; - Активировать режим "только чтение" '
             f'для пользователя.'
             f'\n<u>число</u> - число на которое выдает РО, '
             f'\n<u>время</u> - буквенное обозначение периода (m - минуты, h - часы, d - дни, w - недели).'
             f'\n<i>В случае, если команда передана без аргументов, то режим "только чтение" будет установлен '
             f'по умолчанию на 15 минут.</i>')

    else:
        helping_text: str = \
            (f'Привет, {message.from_user.get_mention()}!'

             f'\n\nСсылка на <b>базовые советы по дипломному проекту:</b>'
             f'<a href="https://magnetic-evergreen-187.notion.site/Python-Basic-3ac614e60b7e434e9d9c018023319c04">'
             f' ТУТ </a>'

             f'\n\nСсылка на <b>видео по подключению к базам данных:</b>'
             f'<a href="https://youtu.be/TCdyfEvrIUg?list=PLA0M1Bcd0w8x4Inr5oYttMK6J47vxgv6J"> перейти в youtube </a>'

             f'\n\nP.S. Итоговая презентация проектов - отменена. '
             f'Вместо неё только защита дипломного проекта перед куратором.\n'
             f'Вы можете посмотреть записи прошедших презентаций по'
             f'<a href="https://docs.google.com/spreadsheets/d/1KbM7aPC4iYcNqm89nUNlQkplxQdfFGYdT2whYgF4V38/edit#gid=0">'
             f' ссылке </a>')

    return helping_text
