import os

# данные для доступа к камерам хранятся в переменных среды, см. readme
camera_turning = os.getenv("camera_turning")  # поворотная камера для тестов
camera_barrier_output = os.getenv("camera_barrier_output")  # камера на шлакбауме наружу
camera_barrier_input = os.getenv("camera_barrier_input")  # камера на шлакбауме внутрь двора

# rtsp потоки от камер
# current_camera = camera_turning  # поворотная камера для тестов
current_camera = camera_barrier_output  # камера на шлакбауме наружу
# current_camera = camera_barrier_input  # камера на шлакбауме внутрь двора

# Параметры для распознавания движения
minimum_contour_size = 50  # размер контура - меньше заданного не реагируем
ball_size_for_remove_noises = 3  # размер ядра для устранения шумов
ball_size_for_for_filling_holes = 3  # размер ядра для заполнения отверстий