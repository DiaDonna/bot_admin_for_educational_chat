import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    @staticmethod
    async def check(message: Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        if isinstance(member, ChatMemberOwner) or isinstance(member, ChatMemberAdministrator):
            return True
        return False

