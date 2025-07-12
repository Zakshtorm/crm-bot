from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from models import Message, session

# ВСТАВЬ СЮДА СВОЙ ТОКЕН 👇
BOT_TOKEN = "7600140579:AAHY2uD9iV1Q1pLLWUJT0eLZNP2GU7N-Nao"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # Сохраняем сообщение в базу
    msg = Message(
        user_id=user.id,
        username=user.username or "unknown",
        text=text
    )
    session.add(msg)
    session.commit()

    await update.message.reply_text("Сообщение сохранено в CRM!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()
