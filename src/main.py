import cv2
import time
from detect_movement import setup_camera, setup_motion_detector, apply_motion_detector, display_frame_with_motion, release_resources, send_telegram_notification, create_time_mask, apply_time_mask
import asyncio

if __name__ == "__main__":
    cap = setup_camera()
    detector_movement = setup_motion_detector()

    last_notification_time = 0  # переменная для хранения времени последнего уведомления

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Создаем маску времени и применяем ее к кадру
        time_mask, time_area_rect = create_time_mask(frame)
        masked_frame = apply_time_mask(frame, time_mask)

        # Рисуем синий прямоугольник вокруг области с временем
        cv2.rectangle(frame, (time_area_rect[0], time_area_rect[1]),
                      (time_area_rect[0] + time_area_rect[2], time_area_rect[1] + time_area_rect[3]), (255, 0, 0), 2)

        # Применяем детектор движения к обработанному кадру
        contours = apply_motion_detector(detector_movement, masked_frame)
        display_frame_with_motion(frame, contours)

        # Если есть контуры, т.е. движение, то отправляем в телеграм
        if contours:
            current_time = time.time()
            # Проверяем, прошло ли достаточно времени с момента последнего уведомления
            if current_time - last_notification_time >= 3:
                # Отправляем уведомление в телеграм
                # asyncio.run(send_telegram_notification(frame, contours))
                last_notification_time = current_time  # обновляем время последнего уведомления

        key = cv2.waitKey(30)
        if key == 27 or key == ord('q'):  # 27 - код клавиши Esc
            break

    release_resources(cap)
