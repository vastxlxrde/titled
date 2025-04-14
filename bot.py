
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from keep_alive import keep_alive

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = 1874218277  # Замените на свой ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📤 Отправить демо", callback_data="send_demo")],
        [InlineKeyboardButton("📩 Обратная связь", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать в бот! 🎵", reply_markup=reply_markup)

async def send_demo_instruction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь трек в mp3 или wav!")

async def handle_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.audio or update.message.voice or update.message.document
    if not file:
        await update.message.reply_text("Отправь аудиофайл, голосовое или документ с треком.")
        return
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="Получена новая демка!")
    await update.message.reply_text("Спасибо! Твоя демка отправлена.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Кнопка нажата.")

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("senddemo", send_demo_instruction))
    application.add_handler(MessageHandler(filters.ATTACHMENT, handle_demo))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.run_polling()
