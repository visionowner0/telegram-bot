import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

BOT_TOKEN = "8962438715:AAF1xOkx8QEdIj_7dkre8sA3tR0e7Am74gY"
REGISTRATION_LINK = "https://t.me/+2dsQzBDy3KAxNTNh"

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    first_name = request.from_user.first_name

    # वेलकम मैसेज + रजिस्ट्रेशन लिंक
    welcome_text = f"हेलो {first_name}! 👋आपकी रिक्वेस्ट मिल गई है, थोड़ी देर में एक्सेप्ट कर ली जाएगी।👉 रजिस्ट्रेशन लिंक: {REGISTRATION_LINK}"
    await context.bot.send_message(chat_id=user_id, text=welcome_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    print("Bot चालू हो गया है...")
    app.run_polling()
