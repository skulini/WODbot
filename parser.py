import os
from telethon import TelegramClient, events
import db

api_id = int(os.getenv(29323351))
api_hash = os.getenv(95bd085296678820b14178fdc4864f2e)
channels = os.getenv(@ccf_38,@CF_bratsk,@kryukovcf).split(",")

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats=channels))
async def handler(event):
    text = event.message.message.lower()
    if "тренировка" in text:
        db.add_workout(event.message.message, "channel")
        print("💾 Сохранено:", event.message.message[:50])

async def main():
    db.init_db()
    await client.start()
    print("✅ Парсер запущен")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
