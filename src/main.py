from detect_movement import setup_camera
from detect_movement import setup_motion_detector
from detect_movement import apply_motion_detector
from detect_movement import display_frame_with_motion
from detect_movement import release_resources
# from detect_movement import send_telegram_notification

import cv2
import time

if __name__ == "__main__":
    cap = setup_camera()
    detector_movement = setup_motion_detector()

    last_notification_time = 0  # переменная для хранения времени последнего уведомления

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        contours = apply_motion_detector(detector_movement, frame)
        display_frame_with_motion(frame, contours)

        # Если есть контуры, т.е. движение, то отправляем в телеграм
        if contours:
            current_time = time.time()
            # Проверяем, прошло ли достаточно времени с момента последнего уведомления
            if current_time - last_notification_time >= 3:
                # send_telegram_notification(frame, contours)
                last_notification_time = current_time  # обновляем время последнего уведомления

        key = cv2.waitKey(30)
        if key == 27 or key == ord('q'):  # 27 - код клавиши Esc
            break

    release_resources(cap)
