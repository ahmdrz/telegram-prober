from telethon.tl.functions.messages import GetHistoryRequest

from telegram.client import start_client, pick_random_client


async def send_message_and_wait_for_reply(target):
    client = pick_random_client()
    await start_client(client)
    entity = await client.peer_manager.get(client, target)
    response = await client.send_message(entity, '/start health_check')
    history_request = GetHistoryRequest(
        peer=entity,
        limit=10,
        offset_date=None,
        offset_id=0,
        min_id=response.id,
        max_id=0,
        add_offset=0,
        hash=0,
    )
    tries = 0
    while tries < 3:
        history = await client(history_request)
        for message in history.messages:
            if message.from_id == response.to_id.user_id:
                return True
        tries += 1
    return False
