import cv2
import os

# Переменные среды для подключения к потоку
rstp_login = os.getenv("rstp_login")
rstp_pass = os.getenv("rstp_pass")
rstp_pass2 = os.getenv("rstp_pass2")

# урлы камер
rtsp_url = f"rtsp://{rstp_login}:{rstp_pass}@89.223.2.11:554/cam/realmonitor?channel=1&subtype=0"  # камера на шлакбауме наружу
# rtsp_url = f"rtsp://{rstp_login}:{rstp_pass}@193.106.98.189/:554/cam/realmonitor?channel=1&subtype=0"  # поворотная камера для тестов
# rtsp_url = f"rtsp://{rstp_login}:{rstp_pass2}@89.223.2.71:554/cam/realmonitor?channel=1&subtype=0"  # камера на шлакбауме внутрь двора
cap = cv2.VideoCapture(rtsp_url)

# Инициализация детектора движения
# history -количество предыдущих кадров, если больше, то будет больший период времени, но медленнее обновляется модель, например последние 100 кадров
# varThreshold - порог, при котором считаем частью фона или переднего плана - если значение слишком низкое, то будут ложные срабатывания
# detectShadows - тени = булевый

# detector_movement= cv2.createBackgroundSubtractorMOG2() # по умолчанию, если без настроек
detector_movement = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=30, detectShadows=False)  # тени вырубил, иначе идут отблески от мокрых машин


while True:
    # Захват кадра из видеопотока
    ret, frame = cap.read()

    # Применение детектора движения
    motion_mask = detector_movement.apply(frame)

    # Применение морфологических операций для улучшения результатов
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, (8, 8))
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, (8, 8))

    # Нахождение контуров движения
    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Перебор контуров и отображение прямоугольников вокруг областей движения
    for contour in contours:
        if cv2.contourArea(contour) > 30:  # Фильтрация небольших контуров
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Отображение кадра с выделенными областями движения
    cv2.imshow("Motion Detection", frame)

    # Выход из цикла по нажатию клавиши 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
