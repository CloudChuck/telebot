from telethon.sync import TelegramClient, events
import os
import time

# ✅ Fetch from environment variables (safe for Render)
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
channel_username = os.environ.get("channel_username")
download_folder = 'downloads'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

with TelegramClient('unified_session', api_id, api_hash) as client:

    # 🔁 Step 1: Download + forward old messages
    print("🔄 Scraping old messages...")

    entity = client.get_entity(channel_username)
    for msg in client.iter_messages(entity, reverse=False):
        if msg.media:
            try:
                file_path = msg.download_media(file=download_folder)
                print(f"✅ Downloaded: {file_path}")
            except Exception as e:
                print(f"❌ Download error: {e}")
        try:
            msg.forward_to('me')
            print(f"➡️ Forwarded: {msg.id}")
        except Exception as e:
            print(f"❌ Forward error: {e}")
        time.sleep(1)

    # ✅ Step 2: Listen for new messages (live mode)
    print("👀 Watching for new messages...")

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        msg = event.message
        if msg.media:
            try:
                file_path = await msg.download_media(file=download_folder)
                print(f"🆕 Downloaded: {file_path}")
            except Exception as e:
                print(f"❌ Real-time Download error: {e}")
        try:
            await msg.forward_to('me')
            print(f"➡️ Real-time Forwarded: {msg.id}")
        except Exception as e:
            print(f"❌ Real-time Forward error: {e}")

    client.run_until_disconnected()
