import sys

from decouple import config
from telethon.sessions import StringSession

from telegram.client import start_client, CustomTelegramClient, PeerManager


def get_client():
    return CustomTelegramClient(
        session=StringSession(session),
        api_hash=config('TELEGRAM_API_HASH'),
        api_id=int(config('TELEGRAM_API_ID')),
        peer_manager=PeerManager(),
    )


client = get_client()
client.loop.run_until_complete(start_client(client, phone=sys.argv[1]))
session = client.session.save()
print(session)
