import os
import threading
from flask import Flask
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Dummy Web Server for Render Web Service
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

# Auto-Reaction Function
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.channel_post:
            await context.bot.set_message_reaction(
                chat_id=update.channel_post.chat_id,
                message_id=update.channel_post.message_id,
                reaction="🔥"
            )
    except Exception as e:
        print(f"Error adding reaction: {e}")

# Join Request Handler Function
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    first_name = request.from_user.first_name

    welcome_text = (
        f"✅Hᴇʟʟᴏ {first_name} ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ🎉\n"
        "Yᴏᴜ Aʀᴇ ᴀ Pʀᴇᴍɪᴜᴍ Uꜱᴇʀ Nᴏᴡ 🧡\n\n"
        "loss recovery fast :- /start\n\n"
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
        print(f"Error sending message to {user_id}: {e}")

def main():
    threading.Thread(target=run_web, daemon=True).start()

    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        print("Error: BOT_TOKEN Environment Variable missing!")
        return

    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))

    application.run_polling()

if __name__ == '__main__':
    main()
