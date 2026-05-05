import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# код -> список видео
data = {}

# временное хранение при добавлении нового кода
temp_storage = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Отправь кодовое слово.")

@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    await message.answer("Напиши: /save код")

@dp.message_handler(commands=['save'])
async def save(message: types.Message):
    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("Пример: /save secret123")
        return

    code = parts[1]
    temp_storage[message.from_user.id] = {
        "code": code,
        "videos": []
    }

    await message.answer("Теперь отправь 2 видео подряд.")

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    user_id = message.from_user.id

    if user_id in temp_storage:
        temp_storage[user_id]["videos"].append(message.video.file_id)

        if len(temp_storage[user_id]["videos"]) == 2:
            code = temp_storage[user_id]["code"]
            data[code] = temp_storage[user_id]["videos"]

            del temp_storage[user_id]

            await message.answer(f"Код '{code}' сохранён.")

@dp.message_handler()
async def check_code(message: types.Message):
    code = message.text.strip()

    if code in data:
        for video_id in data[code]:
            await message.answer_video(video_id)
    else:
        await message.answer("Неверный код.")

if name == "__main__":
    executor.start_polling(dp)
