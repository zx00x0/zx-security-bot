import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# تفعيل اللوق
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ✅ التوكن من Render Environment Variables
TOKEN = os.getenv("8552209530:AAGvXgFphfdsVwX0AahIymqyLZr_0gbO-d8")

if not TOKEN:
    raise ValueError("TOKEN is missing! Add it in Render Environment Variables")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 البوت شغال الآن بنجاح!")

# main function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()