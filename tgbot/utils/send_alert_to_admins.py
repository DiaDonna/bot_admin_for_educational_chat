import asyncio
from contextlib import suppress

from aiogram.types import Message
from aiogram.utils.exceptions import Unauthorized

from tgbot.config import Config
from tgbot.utils.admin_ids import get_admins_ids_for_report
from tgbot.utils.log_config import logger


async def send_alert_to_admins(message: Message, text: str, config: Config) -> None:

    admin_ids: list[int] = await get_admins_ids_for_report(message=message, config=config)

    for admin_id in admin_ids:
        with suppress(Unauthorized):
            await message.bot.send_message(admin_id, text)
            logger.info("Send alert message to admin {admin}".format(admin=admin_id))
            await asyncio.sleep(0.3)
