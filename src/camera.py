import cv2


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def start_capture(self):
        if not self.cap.isOpened():
            raise Exception("Could not open video device")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Could not read frame")
        return frame

    def release(self):
        self.cap.release()