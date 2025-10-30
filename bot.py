import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import web
from aiogram.client.default import DefaultBotProperties

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "8426171093:AAH9_v8WdYARjcfoRnkKC4_3QZnQWU93H2A")
PORT = int(os.environ.get("PORT", 8080))  # Railway автоматически подставит свой порт

logging.basicConfig(level=logging.INFO)

# === ИНИЦИАЛИЗАЦИЯ БОТА ===
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# === КОМАНДА /start ===
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 👋 Добро пожаловать в <b>Cofeeboo</b> ☕\n\n"
        "👉 <a href='https://cofeeboo-bot-production.up.railway.app'>Открыть приложение</a>",
        disable_web_page_preview=True
    )

# === ОБРАБОТКА ВЕБХУКА ===
async def handle(request):
    data = await request.json()
    logging.info(f"📩 update: {data}")
    update = types.Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return web.Response(text="ok")

# === ПРОСТАЯ СТРАНИЦА ДЛЯ ПРОВЕРКИ ===
async def index(request):
    return web.Response(text="☕ Cofeeboo bot is running!", content_type="text/html")

# === СТАРТ/ОСТАНОВКА ===
async def on_startup(app):
    webhook_url = "https://cofeeboo-bot-production.up.railway.app/webhook"
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    logging.info(f"🌍 Webhook установлен: {webhook_url}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# === ЗАПУСК СЕРВЕРА ===
def main():
    app = web.Application()
    app.router.add_post("/webhook", handle)
    app.router.add_get("/", index)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Railway должен увидеть, что сервер слушает порт
    port = int(os.environ.get("PORT", 8080))
    logging.info(f"🚀 Starting server on port {port} ...")

    try:
        web.run_app(app, host="0.0.0.0", port=port)
    except Exception as e:
        logging.error(f"❌ Ошибка запуска сервера: {e}")

if __name__ == "__main__":
    # Добавим обработку ошибок при старте
    try:
        main()
    except Exception as e:
        logging.error(f"🔥 Критическая ошибка при запуске: {e}")
