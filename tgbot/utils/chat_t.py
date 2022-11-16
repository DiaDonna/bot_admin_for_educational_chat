from typing import List

from aiogram.types import ChatType


def chat_types() -> List[ChatType]:
    return [ChatType.GROUP, ChatType.SUPERGROUP]
