from telethon import TelegramClient, events, sync, connection
import asyncio
from utils.config_telegram import api_id, api_hash  # работает с main.py


# Мьютекс для синхронизации доступа к базе данных
db_lock = asyncio.Lock()


async def send_telegram_notification(message, image_path, user_id):
    print(message, image_path, user_id)
    async with db_lock:
        # отправка сообщения и изображения
        async with TelegramClient('session_name', api_id, api_hash) as client:
            # Отправляем сообщение
            await client.send_message(user_id, message)

            # Отправляем изображение
            await client.send_file(user_id, image_path)
