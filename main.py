import os
import threading
from flask import Flask
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

# Dummy Web Server for Render Web Service
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

# Telegram Bot Setup
BOT_TOKEN = "8962438715:AAEZdjcvXvdvZ_ZoOPcYvjeNVoqiVoWcqaU"
REGISTRATION_LINK = "https://t.me/+2dsQzBDy3KAxNTNh"

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    first_name = request.from_user.first_name

    welcome_text = f"हेलो {first_name}! 👋आपकी रिक्वेस्ट मिल गई है, थोड़ी देर में एक्सेप्ट कर ली जाएगी।👉 रजिस्ट्रेशन लिंक: {REGISTRATION_LINK}"
    await context.bot.send_message(chat_id=user_id, text=welcome_text)

if __name__ == '__main__':
    # Start Web Server in a separate thread
    threading.Thread(target=run_web, daemon=True).start()
    
    # Start Telegram Bot
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(ChatJoinRequestHandler(handle_join_request))
    print("Bot चालू हो गया है...")
    app_bot.run_polling()
