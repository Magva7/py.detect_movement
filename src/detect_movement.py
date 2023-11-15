import cv2
import numpy as np
import os
from telethon import TelegramClient, events, sync, connection
import asyncio

# Мьютекс для синхронизации доступа к базе данных
db_lock = asyncio.Lock()

async def send_telegram_notification(frame, contours):
    async with db_lock:
        api_id = os.getenv("telegram_api_id_my_number")
        api_hash = os.getenv("telegram_api_hash_my_number")

        async with TelegramClient('session_name', api_id, api_hash) as client:
            message = 'Обнаружено движение'
            user_id = 6287756332  # id моей второй симки
            await client.send_message(user_id, message)

# Создаем маску для игнорирования области с временем
def create_time_mask(frame):
    height, width, _ = frame.shape
    
    # Определите координаты и размеры области с временем в верхнем правом углу
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
    # Применяем маску кадра
    masked_frame = cv2.bitwise_and(frame, frame, mask=~mask)
    return masked_frame

def setup_camera():
    # данные для доступа к камерам хранятся в переменных среды, см. readme
    camera_turning = os.getenv("camera_turning")  # поворотная камера для тестов
    camera_barrier_output = os.getenv("camera_barrier_output")  # камера на шлакбауме наружу
    camera_barrier_input = os.getenv("camera_barrier_input")  # камера на шлакбауме внутрь двора
    
    # rstp потоки от камер
    rstp_url = camera_turning  # поворотная камера для тестов
    # rstp_url = camera_barrier_output  # камера на шлакбауме наружу
    # rstp_url = camera_barrier_input  # камера на шлакбауме внутрь двора
    cap = cv2.VideoCapture(rstp_url)
    return cap

def display_frame_with_motion(frame, contours, show_window=True):
    # на входе кадр из видеопотока и список контуров
    for contour in contours:
        # Фильтрация контуров по их площади - если уменьшить, то больше мелких объектов,
        # но и больше ложных срабатываний
        # ставил 500, и 300, на заднем фоне не видит, поставил 30, много ложных, выставил 200
        if cv2.contourArea(contour) > 200:
            (x, y, w, h) = cv2.boundingRect(contour)

            # рисуем прямоугольники вокруг областей движения на кадре
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Отображаем получившийся кадр с контурами в окне с именем "Movement Detector" - потом закомментирую, т.к. работать будет на сервере через api
    if show_window:
        cv2.imshow("Movement Detector", frame)

def release_resources(cap):
    # на вход подаем видеопоток cap

    # освобождаем ресурсы
    cap.release()

    # закрываем окна -  - потом закомментирую, т.к. работать будет на сервере через api
    cv2.destroyAllWindows()

def setup_motion_detector():
    # history - количество предыдущих кадров, если больше, то будет больший период времени, но медленнее обновляется модель, например последние 100 кадров
    # varThreshold - порог, при котором считаем частью фона или переднего плана - если значение слишком низкое, то будут ложные срабатывания
    # detectShadows - тени = булевый
    # detector_movement= cv2.createBackgroundSubtractorMOG2() # по умолчанию, если без настроек
    detector_movement = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=30, detectShadows=False)
    return detector_movement

def apply_motion_detector(detector, frame):
    motion_mask = detector.apply(frame)

    # размер ядра для эрозии (удаление малых объектов) и дилатации (заполнение внутренних дыр - если будет пустое внутри)
    # если большие значения, то не будет мелких шумов, но и мелкие объекты не будут находиться
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, (25, 25))

    # размер ядер - сначала дилатация (чтобы маленькие отверстия заполнить), а потом эрозия (удаляет выступающие части)
    # если большие значения, то отверстия будут закрываться, но если задать слишком высоко, то не будут распознаваться мелкие объекты
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, (28, 28))

    # ищем контуры движения по заданной маске
    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours
