import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChatAdministratorRights


class BotPermission(BoundFilter):
    key = 'bot_can_restrict'

    def __init__(self, bot_can_restrict: typing.Optional[bool] = None):
        self.bot_can_restrict = bot_can_restrict

    async def check(self, obj):
        if self.bot_can_restrict is None:
            return False

        rights: ChatAdministratorRights = await obj.bot.get_my_default_administrator_rights()
        return rights.can_restrict_members
