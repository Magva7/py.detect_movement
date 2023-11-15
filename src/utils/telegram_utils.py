import os
import cv2
from telethon import TelegramClient, events, sync, connection
import asyncio

# Мьютекс для синхронизации доступа к базе данных
db_lock = asyncio.Lock()

async def send_telegram_notification(frame, contours):
    async with db_lock:
        api_id = os.getenv("telegram_api_id_my_number")
        api_hash = os.getenv("telegram_api_hash_my_number")

        async with TelegramClient('session_name', api_id, api_hash) as client:
            # Отправляем сообщение
            message = 'Обнаружено движение'
            user_id = 6287756332  # id моей второй симки
            await client.send_message(user_id, message)

            # Рисуем контуры движения на кадре
            frame_with_contours = frame.copy()
            cv2.drawContours(frame_with_contours, contours, -1, (0, 255, 0), 2)

            # Сохраняем кадр с контурами во временный файл
            temp_image_path = 'temp_image.jpg'
            cv2.imwrite(temp_image_path, frame_with_contours)

            # Отправляем изображение в телеграм
            await client.send_file(user_id, temp_image_path)

            # Удаляем временный файл
            os.remove(temp_image_path)
