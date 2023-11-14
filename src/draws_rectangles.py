import cv2

def display_frame_with_motion(frame, contours):
    # на входе кадр из видеопотока и список контуров
    for contour in contours:
        # Фильтрация контуров по их площади - если уменьшить, то больше мелких объектов,
        # но и больше ложных срабатываний
        # ставил 500, и 300, на заднем фоне не видит, поставил 30, потом 200
        if cv2.contourArea(contour) > 200:
            (x, y, w, h) = cv2.boundingRect(contour)

            # рисуем прямоугольники вокруг областей движения на кадре
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Отображаем получившийся кадр с контурами в окне с именем "Movement Detector".
    cv2.imshow("Movement Detector", frame)

def release_resources(cap):
    # на вход подаем видеопоток cap

    # освобождаем ресурсы
    cap.release()

    # закрываем окна
    cv2.destroyAllWindows()
