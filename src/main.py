from detect_movement import setup_camera
from detect_movement import setup_motion_detector
from detect_movement import apply_motion_detector
from detect_movement import display_frame_with_motion
from detect_movement import release_resources

import cv2

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
