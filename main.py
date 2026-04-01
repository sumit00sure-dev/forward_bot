import asyncio
from telethon import TelegramClient, events, Button
from config import *
from database import *
from processor import process_caption
from queue_manager import QUEUE, worker

print("BOT TOKEN:", BOT_TOKEN)
print("API ID:", API_ID)
print("API HASH:", API_HASH)

client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ✅ Admin Check
def is_admin(user):
    return user == ADMIN_ID

# 🔹 Add Mapping
@client.on(events.NewMessage(pattern="/addmap"))
async def addmap(event):
    if not is_admin(event.sender_id):
        return
    try:
        _, src, tgt = event.text.split()
        add_map(src, tgt)
        await event.reply("✅ Mapping Added")
    except:
        await event.reply("Usage: /addmap source target")

# 🔹 Remove Mapping
@client.on(events.NewMessage(pattern="/removemap"))
async def removemap(event):
    if not is_admin(event.sender_id):
        return
    try:
        _, src, tgt = event.text.split()
        remove_map(src, tgt)
        await event.reply("❌ Mapping Removed")
    except:
        await event.reply("Usage: /removemap source target")

# 🔹 Stats
@client.on(events.NewMessage(pattern="/stats"))
async def stats(event):
    if not is_admin(event.sender_id):
        return
    db = load()
    await event.reply(f"Processed: {db['stats']['processed']}")

# 🔥 MAIN HANDLER (CORE)
@client.on(events.NewMessage)
async def handler(event):
    source = str(event.chat_id)
    targets = get_targets(source)

    if not targets:
        return

    async def process():
        caption = process_caption(event.text)

        buttons = [
            [Button.url("🔒 Join Backup", BACKUP_CHANNEL)]
        ]

        for target in targets:
            retry = 0
            while retry < MAX_RETRY:
                try:
                    await client.send_message(
                        int(target),
                        message=caption,
                        file=event.media,
                        buttons=buttons
                    )
                    inc_stats()
                    break
                except Exception as e:
                    retry += 1
                    await asyncio.sleep(1)

    await QUEUE.put(process)

# 🚀 START
async def main():
    for _ in range(5):
        asyncio.create_task(worker())

    print("🚀 Ultra Bot Running...")
    await client.run_until_disconnected()

client.loop.create_task(main())
client.run_until_disconnected()
