import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
import openai
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_HOST = os.getenv("WEBHOOK_URL")  # Например, https://your-app.onrender.com
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT", 3000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

def generate_congrats(name, relation):
    prompt = (
        f"Придумай поздравление с днём рождения для {name}. "
        f"Этот человек — {relation}. Стиль: тёплый, дружеский, без пафоса. "
        f"Не более 3 предложений."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=100
    )
    return response["choices"][0]["message"]["content"]

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Напиши имя и кто этот человек (пример: Маша, подруга)")

@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        name, relation = [s.strip() for s in message.text.split(",")]
        congrats = generate_congrats(name, relation)
        await message.answer(f"Вот поздравление для {name}:

{congrats}")
    except:
        await message.answer("Пожалуйста, отправь в формате: Имя, кто он тебе. Пример: Алексей, брат")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
