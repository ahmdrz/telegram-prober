import asyncio
import os
import random
import typing

from decouple import config
from telethon import TelegramClient, utils
from telethon.sessions import StringSession, Session


class PeerManager:
    def __init__(self):
        self._peers = dict()

    async def get(self, client, target):
        lock = asyncio.Lock()
        async with lock:
            if target in self._peers:
                return self._peers[target]
            peer = utils.get_input_peer(await client.get_input_entity(target))
            self._peers[target] = peer
            return peer


class CustomTelegramClient(TelegramClient):
    def __init__(self, session: 'typing.Union[str, Session]', api_id: int, api_hash: str):
        super().__init__(session, api_id, api_hash)
        self.peer_manager = PeerManager()


async def start_client(client, phone=None):
    await client.start(phone=phone if phone else lambda: '')


def get_all_sessions():
    telethon_sessions = os.getenv('TELETHON_SESSIONS', '').split(',')
    return telethon_sessions


def pick_random_client() -> CustomTelegramClient:
    telethon_sessions = get_all_sessions()
    random_session = random.randrange(0, len(telethon_sessions))
    client_session_string = telethon_sessions[random_session]
    return get_client(client_session_string)


def get_client(session=None) -> CustomTelegramClient:
    return CustomTelegramClient(
        session=StringSession(session),
        api_hash=config('TELEGRAM_API_HASH'),
        api_id=int(config('TELEGRAM_API_ID')),
    )
