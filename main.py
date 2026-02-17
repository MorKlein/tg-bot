import asyncio
from datetime import date

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, Text
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zoneinfo import ZoneInfo

TOKEN = "8537666175:AAGYYilnU6Q-MhLyg9vBnkNOJl6LNZtCQqA"
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

@dp.message(Text(contains="егэ", ignore_case=True))
async def hello_reply(message: Message):
    await bot.send_message(CHAT_ID, "КТО-ТО СКАЗАЛ ЕГЭ??? ЕГЭ СКОРО!!!")
    await send_daily_message()


@dp.message(Command(commands=["days"]))
async def cmd_days(message: Message):
    await send_daily_message()


async def main():
    scheduler.add_job(send_daily_message, "cron", hour=8, minute=0)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена!")
