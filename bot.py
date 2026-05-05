import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

data = {}
temp = {}

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Отправь кодовое слово.")

@dp.message(F.text.startswith("/save"))
async def save(message: Message):
    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("Пример: /save code123")
        return

    code = parts[1]
    temp[message.from_user.id] = {"code": code, "videos": []}

    await message.answer("Отправь 2 видео подряд.")

@dp.message(F.video)
async def video(message: Message):
    uid = message.from_user.id

    if uid in temp:
        temp[uid]["videos"].append(message.video.file_id)

        if len(temp[uid]["videos"]) == 2:
            data[temp[uid]["code"]] = temp[uid]["videos"]
            del temp[uid]
            await message.answer("Код сохранён.")

@dp.message()
async def check(message: Message):
    code = message.text.strip()

    if code in data:
        for v in data[code]:
            await message.answer_video(v)
    else:
        await message.answer("Неверный код.")

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
