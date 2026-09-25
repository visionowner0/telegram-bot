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

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Credentials from Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

# Dummy Web Server for Render
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

# --- TELEGRAM BOT (Primary Bot) HANDLERS ---

# Primary Bot Auto-Reaction
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.channel_post:
            await context.bot.set_message_reaction(
                chat_id=update.channel_post.chat_id,
                message_id=update.channel_post.message_id,
                reaction="🔥"
            )
    except Exception as e:
        logging.error(f"Bot reaction error: {e}")

# Join Request Handler Function
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    first_name = request.from_user.first_name

    welcome_text = (
        f"✅Hᴇʟʟᴏ {first_name} ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ🎉\n"
        "Yᴏᴜ Aʀᴇ ᴀ Pʀᴇᴍɪᴜᴍ Uꜱᴇʀ Nᴏᴡ 🧡\n\n"
        "Loss Recovery :- Join Nᴏᴡ \n\n"
        "Jᴏɪɴ ʜᴇʀᴇ 📌(ᴇxᴘɪʀᴇ ɪɴ 5 ᴍɪɴᴜᴛᴇꜱ)"
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
    except Exception as e:
        logging.error(f"Error sending message to {user_id}: {e}")

# Global Error Handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error("Exception while handling an update:", exc_info=context.error)


# --- TELETHON USERBOT (Secondary ID) SETUP ---

telethon_client = None
if API_ID and API_HASH:
    try:
        telethon_client = TelegramClient('userbot_session', int(API_ID), API_HASH)

        @telethon_client.on(events.NewMessage)
        async def userbot_reaction_handler(event):
            # If a new post comes in a channel where the userbot is present
            if event.is_channel:
                try:
                    # Send a secondary reaction (e.g., 👍) from the secondary ID
                    await telethon_client.send_reaction(event.chat_id, event.id, "👍")
                except Exception as e:
                    logging.error(f"Userbot reaction error: {e}")
    except Exception as e:
        logging.error(f"Failed to initialize Telethon client: {e}")


# --- MAIN RUNNER ---

def main():
    threading.Thread(target=run_web, daemon=True).start()

    if not BOT_TOKEN:
        logging.error("BOT_TOKEN missing!")
        return

    # Initialize Primary Bot Application
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .get_updates_read_timeout(42.0)
        .build()
    )

    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_error_handler(error_handler)

    print("Bot chalu ho gaya hai...")

    # Start primary bot in polling mode with drop_pending_updates
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
