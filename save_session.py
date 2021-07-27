import sys

from telegram.client import get_client, start_client

client = get_client()
client.loop.run_until_complete(start_client(client, phone=sys.argv[1]))
session = client.session.save()
print(session)
