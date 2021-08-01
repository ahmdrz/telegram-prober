import time

from decouple import config
from telethon.tl.functions.messages import GetHistoryRequest

from telegram.client import start_client


async def send_message_and_wait_for_reply(client, target):
    await start_client(client)
    entity = await client.peer_manager.get(client, target)

    response = await client.send_message(entity, '/start health_check')
    start_time = time.time()

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
    resolution = float(config('REPLY_RESOLUTION', 1))
    timeout = int(config('REPLY_TIMEOUT', '30')) * (1 / resolution)
    while timeout > 0:
        history = await client(history_request)
        for message in history.messages:
            if message.from_id == response.to_id.user_id:
                return True, time.time() - start_time
        timeout -= 1
        time.sleep(resolution)
    return False, None
