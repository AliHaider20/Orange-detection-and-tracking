import cv2
import numpy as np
import matplotlib.pyplot as plt
from Orange_detector import OrangeDetector


class KalmanFilter:
    def __init__(self):
        # Initializing Kalman filter with it's parameters
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array(
            [[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32
        )

    def predict(self, coordX, coordY):
        """
        Estimates position of the object
        """
        measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        x, y = int(predicted[0]), int(predicted[1])
        return x, y


cap = cv2.VideoCapture("Orange.mp4")

od = OrangeDetector()  # Detecting Orange using orange color.

kf = KalmanFilter()

actual_x, actual_y = [], []
x_hat, y_hat = [], []

out = cv2.VideoWriter(
    "Tracking.avi",
    cv2.VideoWriter_fourcc(*"XVID"),
    20,
    (1280, 720),
    isColor=True,
)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if ret:

        box = od.detect(frame)
        x, y, x2, y2 = box
        cx = int((x + x2) / 2)
        cy = int((y + y2) / 2)

        predicted = kf.predict(cx, cy)
        cv2.circle(frame, (cx, cy), 10, (0, 255, 255), -1)
        cv2.circle(frame, (predicted[0], predicted[1]), 10, (255, 0, 0), 4)
        actual_x.append(x)
        actual_y.append(y)
        x_hat.append(predicted[0])
        y_hat.append(predicted[1])
        out.write(frame)
        if cv2.waitKey(15) & 0xFF == ord("q"):
            break
    else:
        break


# plt.plot(actual_x, actual_y)
# plt.plot(x_hat, y_hat)
# plt.show()

cap.release()
out.release()
cv2.destroyAllWindows()
