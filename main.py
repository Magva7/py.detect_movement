import cv2

from src.camera_setting import setup_camera
from src.movement_detector import setup_motion_detector, apply_motion_detector
from src.draws_rectangles import display_frame_with_motion, release_resources

if __name__ == "__main__":
    cap = setup_camera()
    detector_movement = setup_motion_detector()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        contours = apply_motion_detector(detector_movement, frame)
        display_frame_with_motion(frame, contours)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    release_resources(cap)
