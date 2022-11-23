import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import AllowedUpdates

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter

from tgbot.handlers.admin.admin import register_admin
from tgbot.handlers.admin.ban_to_user import register_bun
from tgbot.handlers.admin.ro_to_user import register_ro
from tgbot.handlers.for_incorrect_using_commands import register_incorrect_using_command
from tgbot.handlers.for_private.for_private import register_echo
from tgbot.handlers.groups.hastebin import register_paste_command
from tgbot.handlers.groups.report import register_report_command
from tgbot.handlers.groups.user import register_user
from tgbot.handlers.groups.new_member_info import register_new_member_info
from tgbot.handlers.groups.help_command import register_help_command
from tgbot.middlewares.check_groups import VerifiedGroupsMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.utils.log_config import logger


def register_all_middlewares(dp, config):
    dp.setup_middleware(LoggingMiddleware())
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(VerifiedGroupsMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_incorrect_using_command(dp)

    register_admin(dp)
    register_bun(dp)
    register_ro(dp)

    register_user(dp)
    register_echo(dp)
    register_help_command(dp)
    register_new_member_info(dp)
    register_paste_command(dp)
    register_report_command(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            allowed_updates=(AllowedUpdates.MESSAGE
                             or AllowedUpdates.CHAT_MEMBER
                             or AllowedUpdates.CALLBACK_QUERY
                             or AllowedUpdates.EDITED_MESSAGE))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
