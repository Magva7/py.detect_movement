import cv2
import os

def setup_camera():
    camera_turning = os.getenv("camera_turning")
    camera_barrier_output = os.getenv("camera_barrier_output")
    camera_barrier_input = os.getenv("camera_barrier_input")
    
    # rstp_url = camera_turning  # поворотная камера для тестов
    rstp_url = camera_barrier_output  # камера на шлакбауме наружу
    # rstp_url = camera_barrier_input  # камера на шлакбауме внутрь двора
    cap = cv2.VideoCapture(rstp_url)
    return cap