import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI
import logging

# 🔹 لاگ‌گرفتن برای دیباگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# 🔹 کلیدها از متغیرهای محیطی
TG_BOT_TOKEN ="8291380229:AAGiwOhhtcLMOmDBS2kb69zHkULJHPIY1bk"
OPENAI_API_KEY = "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"


if not TG_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ لطفاً TG_BOT_TOKEN و OPENAI_API_KEY رو ست کنید.")

# 🔹 تنظیم کلاینت OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# فقط آی‌دی‌های مجاز
ALLOWED_USERS = {6951571381, 6885861774}  # آیدی عددی خودت و دوستت رو اینجا بذار

async def chat_with_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("🚫 شما اجازه استفاده از این ربات رو ندارید.")
        return

    user_message = update.message.text

    try:
        # درخواست به OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": user_message}],
        )
        bot_reply = response.choices[0].message.content

        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("❌ خطا در ارتباط با هوش مصنوعی.")
        logging.error(f"OpenAI error: {e}")

def main():
    app = Application.builder().token(TG_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))
    app.run_polling()

if __name__ == "__main__":
    main()

