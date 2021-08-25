import asyncio
import os
import typing

from decouple import config
from telethon import TelegramClient, utils
from telethon.sessions import StringSession, Session


class PeerManager:
    def __init__(self):
        self._peers = dict()
        self._lock = asyncio.Lock()

    async def get(self, client, target):
        async with self._lock:
            if target in self._peers:
                return self._peers[target]
            peer = utils.get_input_peer(await client.get_input_entity(target))
            self._peers[target] = peer
            return peer


class CustomTelegramClient(TelegramClient):
    def __init__(self, session: 'typing.Union[str, Session]', api_id: int, api_hash: str, peer_manager: PeerManager):
        super().__init__(session, api_id, api_hash)
        self.peer_manager = peer_manager


async def start_client(client, phone=None):
    await client.start(phone=phone if phone else lambda: '')


def get_all_sessions():
    telethon_sessions = os.getenv('TELETHON_SESSIONS', '').split(',')
    return telethon_sessions


class Manager:
    def __init__(self):
        self._sessions = get_all_sessions()
        self._peer_managers = [
            PeerManager()
            for _ in self._sessions
        ]
        self._index = 0
        self._lock = asyncio.Lock()

    async def get_next(self):
        async with self._lock:
            session = self._sessions[self._index]
            client = CustomTelegramClient(
                session=StringSession(session),
                api_hash=config('TELEGRAM_API_HASH'),
                api_id=int(config('TELEGRAM_API_ID')),
                peer_manager=self._peer_managers[self._index]
            )
            self._index += 1
            if self._index >= len(self._sessions):
                self._index = 0
        return client


manager_instance = Manager()
