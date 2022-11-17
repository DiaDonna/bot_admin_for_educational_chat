from contextlib import suppress

from aiogram import md, types, Dispatcher
from aiogram.types.chat_member import ChatMemberAdministrator, ChatMemberOwner
from aiogram.utils.exceptions import TelegramAPIError
from magic_filter import F

from tgbot.config import Config
from tgbot.utils.chat_t import chat_types
from tgbot.utils.hastebin import get_hastebin_client


async def command_paste(message: types.Message, config: Config):
    """
    Хендлер для комманды /paste
    Используется для вставки сообщения на hastebin сервер

    Handler for command /paste
    Can be used for sending message to hastebin server
    """
    messages_to_delete = []
    if message.reply_to_message and message.reply_to_message.from_user.id != message.bot.id:
        content = message.reply_to_message.text or message.reply_to_message.caption
        dst = message.reply_to_message
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        if isinstance(member, ChatMemberOwner) or (
                isinstance(member, ChatMemberAdministrator) and member.can_delete_messages
        ):
            messages_to_delete.append(dst)
    else:
        content = message.get_args()
        dst = message
        messages_to_delete.append(dst)

    if not content or (len(content) < 30 and content.count('\n') < 2):
        return await message.reply("Слишком короткий текст!")

    content = content.encode()
    response = await get_hastebin_client(config.misc.hastebin_url).create_document(content)

    document_url = get_hastebin_client(config.misc.hastebin_url).format_url(response["key"])
    text = "Сообщение опубликованное {author} было перемещено в {url}\n" \
           "Размер: {size} байт".format(
        author=dst.from_user.get_mention(as_html=True),
        url=md.hlink("HasteBin", document_url),
        size=len(content),
    )
    await dst.reply(text, allow_sending_without_reply=True)

    for message_to_delete in messages_to_delete:
        with suppress(TelegramAPIError):
            await message_to_delete.delete()


def register_paste_command(dp: Dispatcher):
    dp.register_message_handler(command_paste,
                                F.ilter(F.reply_to_message),
                                chat_type=chat_types(),
                                commands=['paste'],
                                state='*')
