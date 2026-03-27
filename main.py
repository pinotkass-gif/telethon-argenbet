import os
import asyncio
import aiohttp
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK")

client = TelegramClient.parse_session_string(SESSION_STRING, API_ID, API_HASH) if SESSION_STRING else None

async def send_to_n8n(sender_id, username, text):
    async with aiohttp.ClientSession() as session:
        payload = {
            "telegram_id": str(sender_id),
            "username": username or "",
            "mensaje": text or ""
        }
        await session.post(N8N_WEBHOOK, json=payload)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        sender = await event.get_sender()
        await send_to_n8n(sender.id, sender.username, event.text)

async def main():
    await client.start()
    print("Telethon corriendo...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
