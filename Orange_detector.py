import cv2
import numpy as np
from util import get_limits


class OrangeDetector:
    def __init__(self):
        # Lower and uppler limit of the HSV value of the color.
        self.loworange = np.array([6, 100, 100])
        self.highorange = np.array([20, 255, 255])

    def detect(self, img):
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Creating a mask of pixels within the low and upper value range.
        mask = cv2.inRange(hsv_image, self.loworange, self.highorange)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        box = (-100, -100, 0, 0)
        for cnt in contours:
            # Fetching the co-ordinates of the contours.
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w * h > 300:
                box = (x, y, x + w, y + h)
                break

        return box
