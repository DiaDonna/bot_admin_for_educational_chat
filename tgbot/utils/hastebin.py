from typing import Dict, Any
from urllib.parse import urljoin

from aiohttp import ClientSession

from tgbot import config


class HasteBinClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = ClientSession()

    def format_url(self, uri: str) -> str:
        return urljoin(self.base_url, uri)

    async def create_document(self, content: bytes) -> Dict[str, Any]:
        response = await self.session.post(url=self.format_url("/documents"), data=content)
        response.raise_for_status()
        result = await response.json()
        await self.session.close()
        return result


def get_hastebin_client(url):
    return HasteBinClient(url)
