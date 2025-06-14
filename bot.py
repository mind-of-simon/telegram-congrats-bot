import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши имя и кто этот человек (пример: Маша, подруга)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        name, relation = [s.strip() for s in text.split(",", 1)]
        prompt = f"Придумай короткое поздравление с днём рождения для {name}. Этот человек — {relation}. Стиль: тёплый, дружеский, без пафоса. Не более 3 предложений."
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9,
    max_tokens=100
)
message = response["choices"][0]["message"]["content"]
await update.message.reply_text(f"Вот поздравление для {name}:\n\n{message}")


{message}")
    except:
        await update.message.reply_text("Пожалуйста, отправь в формате: Имя, кто он тебе. Пример: Алексей, брат")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
