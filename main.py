import os
import threading
import logging
import asyncio
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Credentials from Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING", "")  # For Telethon userbot login

# Dummy Web Server for Render
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

# --- PRIMARY BOT (AUTO-REACTION & WELCOME MESSAGE) ---

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.channel_post:
            await context.bot.set_message_reaction(
                chat_id=update.channel_post.chat_id,
                message_id=update.channel_post.message_id,
                reaction="🔥"
            )
            logging.info("Primary bot post reaction success!")
    except Exception as e:
        logging.error(f"Bot reaction error: {e}")

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    first_name = request.from_user.first_name

    welcome_text = (
        f"✅Hᴇʟʟᴏ {first_name} ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ🎉\n"
        "Yᴏᴜ Aʀᴇ ᴀ PʀᴇᴍɪᴜM UꜱᴇR Nᴏᴡ 🧡\n\n"
        "Loss Recovery :- Join Nᴏᴡ \n\n"
        "Jᴏɪɴ ʜᴇʀᴇ 📌(ᴇxᴘɪRᴇ ɪɴ 5 ᴍɪɴᴜᴛᴇꜱ)"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text="📌 Join Channel Now", 
                url="https://t.me/+-yN02-S6eQY2MjBh"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=welcome_text,
            reply_markup=reply_markup
        )
        logging.info(f"Welcome message sent to {user_id}")
    except Exception as e:
        logging.error(f"Error sending welcome message to {user_id}: {e}")

# --- TELETHON USERBOT BACKGROUND WORKER ---

def start_telethon_userbot():
    if not (API_ID and API_HASH and SESSION_STRING):
        logging.warning("Telethon skipped: SESSION_STRING or API credentials missing.")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)

        @client.on(events.NewMessage)
        async def userbot_reaction_handler(event):
            if event.is_channel:
                try:
                    await client.send_reaction(event.chat_id, event.id, "👍")
                    logging.info("Secondary userbot reaction success!")
                except Exception as e:
                    logging.error(f"Userbot reaction error: {e}")

        logging.info("Starting Telethon userbot...")
        client.start()
        client.run_until_disconnected()
    except Exception as e:
        logging.error(f"Telethon userbot crashed: {e}")

# --- MAIN EXECUTOR ---

def main():
    # Start Flask server
    threading.Thread(target=run_web, daemon=True).start()

    # Start Telethon Userbot only if session exists
    threading.Thread(target=start_telethon_userbot, daemon=True).start()

    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is missing!")
        return

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))

    logging.info("Primary Telegram Bot is polling...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
