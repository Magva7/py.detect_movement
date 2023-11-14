import cv2

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
