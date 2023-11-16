import cv2
import numpy as np
import os
from telethon import TelegramClient, events, sync, connection
import asyncio
from utils.config_telegram import api_id, api_hash  # получение айди и хэша нашего приложения из файла config.py
from stream_setting import current_camera, minimum_contour_size, ball_size_for_remove_noises, ball_size_for_for_filling_holes

# Мьютекс для синхронизации доступа к базе данных
db_lock = asyncio.Lock()

# функция для отправки оповещения в телеграм
async def send_telegram_notification(frame, contours):
    async with db_lock:
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

# Создаю маску для игнорирования области с временем, которая в углу
def create_time_mask(frame):
    height, width, _ = frame.shape
    
    # Координаты и размеры области с временем в верхнем правом углу, которую будем игнорировать
    time_area_x = width - 320  # примерные координаты X
    time_area_y = 0  # примерные координаты Y
    time_area_width = 320  # примерная ширина области
    time_area_height = 80  # примерная высота области
    
    # Создаем черное изображение маски
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # Заполняем белым цветом область с временем
    mask[time_area_y:time_area_y + time_area_height, time_area_x:time_area_x + time_area_width] = 255
    
    return mask, (time_area_x, time_area_y, time_area_width, time_area_height)

# Применяем маску перед обработкой детектором движения
def apply_time_mask(frame, mask):
    # Инвертируем маску перед применением, т.е. движение же будем искать не внутри маски, а наоброт снаружи
    inverted_mask = cv2.bitwise_not(mask)
    # Применяем инвертированную маску кадра
    masked_frame = cv2.bitwise_and(frame, frame, mask=inverted_mask)
    return masked_frame

def setup_camera():
    cap = cv2.VideoCapture(current_camera)
    return cap

def display_frame_with_motion(frame, contours, show_window=True):
    # на входе кадр из видеопотока и список контуров
    for contour in contours:
        # Фильтрация контуров по их площади
        if cv2.contourArea(contour) > minimum_contour_size:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Отображаем получившийся кадр с контурами в окне
    if show_window:
        cv2.imshow("Movement Detector", frame)

def release_resources(cap):
    cap.release()
    cv2.destroyAllWindows()

def setup_motion_detector():
    # Создаем детектор движения
    detector_movement = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=30, detectShadows=False)
    return detector_movement

def apply_motion_detector(detector, frame):
    motion_mask = detector.apply(frame)
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, (ball_size_for_remove_noises, ball_size_for_remove_noises))
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, (ball_size_for_for_filling_holes, ball_size_for_for_filling_holes))

    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours
