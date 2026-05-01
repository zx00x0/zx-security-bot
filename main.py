from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import logging
import os

TOKEN = os.getenv("8552209530:AAGvXgFphfdsVwX0AahIymqyLZr_0gbO-d8")

logging.basicConfig(level=logging.INFO)

FORBIDDEN_WORDS = ["اختراق","هكر","virus","hack","ddos","phishing"]

def check_safety(text):
    text_lower = text.lower()
    for w in FORBIDDEN_WORDS:
        if w in text_lower:
            return False, w
    return True, None

# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    welcome = f"""🤖 أهلاً {user.first_name}

أنا ZX Coding Assistant

💻 أساعدك في البرمجة
🔐 وأرفض أي شيء غير قانوني

اكتب /help"""

    keyboard = [
        [InlineKeyboardButton("💻 كود", callback_data="code"),
         InlineKeyboardButton("🔍 شرح", callback_data="explain")],
        [InlineKeyboardButton("📚 لغات", callback_data="languages"),
         InlineKeyboardButton("🔐 أمن", callback_data="security")]
    ]

    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))

# ========== HELP ==========
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
/start - تشغيل
/help - مساعدة
/code - كود
""")

# ========== CODE ==========
async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("استخدم: /code python hello")
        return

    lang = context.args[0]
    task = context.args[1]

    safe, word = check_safety(" ".join(context.args))
    if not safe:
        await update.message.reply_text(f"🚫 ممنوع: {word}")
        return

    codes = {
        "python": "print('Hello World')",
        "javascript": "console.log('Hello')"
    }

    result = codes.get(lang, "❌ غير موجود")

    await update.message.reply_text(f"💻 {result}")

# ========== HANDLE ==========
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    safe, word = check_safety(update.message.text)
    if not safe:
        await update.message.reply_text("🚫 ممنوع")
        return

    await update.message.reply_text("استخدم /help")

# ========== BUTTONS ==========
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "code":
        await q.edit_message_text("اكتب /code python hello")
    elif q.data == "security":
        await q.edit_message_text("🔐 أنا أمن فقط أخلاقي")

# ========== MAIN ==========
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("code", code))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()