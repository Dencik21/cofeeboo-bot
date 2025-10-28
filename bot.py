import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8426171093:AAH9_v8WdYARjcfoRnkKC4_3QZnQWU93H2A"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# --- Команда /start ---
@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💫 О нас", callback_data="about"),
                InlineKeyboardButton(text="📞 Контакты", callback_data="contact")
            ],
            [
                InlineKeyboardButton(text="❓ Помощь", callback_data="help")
            ]
        ]
    )
    await message.answer(
        "Привет! 👋 Я твой Telegram-бот.\nВыбери действие ниже:",
        reply_markup=keyboard
    )

# --- Обработка нажатий на кнопки ---
@dp.callback_query()
async def handle_buttons(callback: types.CallbackQuery):
    if callback.data == "about":
        await callback.message.answer("✨ Я демонстрационный бот, созданный на Python с помощью Aiogram!")
    elif callback.data == "contact":
        await callback.message.answer("📩 Связаться со мной можно по email: example@example.com")
    elif callback.data == "help":
        await callback.message.answer("❓ Просто нажми кнопку или напиши команду, чтобы я ответил!")
    await callback.answer()

# --- Команда /help ---
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Я могу отвечать на команды:\n/start — начать\n/help — помощь")

# --- Ответ на любые сообщения ---
@dp.message()
async def echo_message(message: Message):
    await message.answer(f"Ты написал: {message.text}")

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
