import asyncio
import os
from datetime import date

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zoneinfo import ZoneInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не найден! Проверьте переменные окружения.")

CHAT_ID = -907901634  # id чата или канала
Chemistry = date(2026, 6, 1)
Math = date(2026, 6, 4)
Russian = date(2026, 6, 8)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()
router = Router()
dp.include_router(router)
scheduler = AsyncIOScheduler(
    timezone=ZoneInfo("Europe/Moscow")
)

def calculate_days(target):
    today = date.today()
    delta = target - today
    return delta.days

@router.message()
async def get_chat_id(message: Message):
    await message.answer(f"Chat ID: {message.chat.id}")


async def send_daily_message():
    days_left = calculate_days(Chemistry)
    text = f"⏳ До ЕГЭ по химии осталось <b>{days_left}</b> дней!"
    await bot.send_message(CHAT_ID, text)
    days_left = calculate_days(Russian)
    text = f"⏳ До ЕГЭ по русскому осталось <b>{days_left}</b> дней!"
    await bot.send_message(CHAT_ID, text)
    days_left = calculate_days(Math)
    text = f"⏳ До ЕГЭ по математике осталось <b>{days_left}</b> дней!"
    await bot.send_message(CHAT_ID, text)

TRIGGER_WORDS = ["егэ"]

@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text.lower()  # приводим к нижнему регистру для удобства
    for word in TRIGGER_WORDS:
        if word in text:
            await message.reply(f"КТО_ТО СКАЗАЛ ЕГЭ??? ЕГЭ УЖЕ СКОРО!!!")
            await send_daily_message()
            break  # чтобы реагировать только на первое найденное слово


@dp.message(Command(commands=["days"]))
async def cmd_days(message: Message):
    await send_daily_message()


async def main():
    logger.info("Запуск бота...")
    logger.info("BOT_TOKEN: %s...", TOKEN[:5])
    scheduler.add_job(send_daily_message, "cron", hour=8, minute=0)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена!")






