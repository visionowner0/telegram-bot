import os
import threading
from flask import Flask
import logging
from telegram import Update
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

# Telegram Bot Settings
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8962438715:AAF1xOkx8QEdIj_7dkre8sA3tR0e7Am74gY")
REGISTRATION_LINK = "https://t.me/+2dsQzBDy3KAxNTNh"

# 1. Join Request Handler
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    first_name = request.from_user.first_name

    welcome_text = f"हेलो {first_name}! 👋आपकी रिक्वेस्ट मिल गई है, थोड़ी देर में एक्सेप्ट कर ली जाएगी।👉 रजिस्ट्रेशन लिंक: {REGISTRATION_LINK}"
    await context.bot.send_message(chat_id=user_id, text=welcome_text)

# 2. Channel Post Auto-Reaction Handler
async def auto_react_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        chat_id = update.channel_post.chat_id
        message_id = update.channel_post.message_id
        
        try:
            # Bot post par 🔥 reaction karega (Aap reaction="❤️" bhi kar sakte hain)
            await context.bot.set_message_reaction(
                chat_id=chat_id,
                message_id=message_id,
                reaction="🔥"
            )
        except Exception as e:
            print(f"Reaction Error: {e}")

if __name__ == '__main__':
    # Start Web Server in background thread
    threading.Thread(target=run_web, daemon=True).start()
    
    # Start Telegram Bot
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers Add Karein
    app_bot.add_handler(ChatJoinRequestHandler(handle_join_request))
    app_bot.add_handler(MessageHandler(filters.ChatType.CHANNEL, auto_react_channel_post))
    
    print("Bot chalu ho gaya hai...")
    app_bot.run_polling()
