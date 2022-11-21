from aiogram import Bot
from aiogram.types import Message, ChatMemberAdministrator, ChatMemberOwner

from tgbot.config import Config


async def get_admins_ids_for_report(message: Message, config: Config) -> list[int]:
    """
    Возвращает id админов группы, с id владельца или без него, зависит от параметра send_report_to_owner
    """
    bot: Bot = message.bot
    send_report_to_owner: bool = config.tg_bot.send_report_to_owner
    admins: list[ChatMemberOwner | ChatMemberAdministrator] = await bot.get_chat_administrators(message.chat.id)
    admin_ids: list[int] = []
    for admin in admins:
        if not send_report_to_owner:
            if not admin.is_chat_owner() and not admin.user.is_bot:
                admin_ids.append(admin.user.id)
        elif not admin.user.is_bot:
            admin_ids.append(admin.user.id)
    return admin_ids


async def get_admins_ids_for_help(message: Message) -> list[int]:
    """
    Возвращает id админов группы, включая владельца группы
    """
    bot: Bot = message.bot
    admins: list[ChatMemberOwner | ChatMemberAdministrator] = await bot.get_chat_administrators(message.chat.id)
    admin_ids: list[int] = []
    for admin in admins:
        if not admin.user.is_bot:
            admin_ids.append(admin.user.id)

    return admin_ids
