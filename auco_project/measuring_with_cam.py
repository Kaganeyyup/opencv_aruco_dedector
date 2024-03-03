import cv2
import cv2 as cv
from dedektor import *
import numpy as np


parameters = cv2.aruco.DetectorParameters()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

detector = HomogeneousBgDetector()

cap = cv2.VideoCapture(0)  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, img = cap.read()  

    corners, _a, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if corners:

        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)


        aruco_perimeter = cv2.arcLength(corners[0], True)


        pixel_cm_ratio = aruco_perimeter / 20

        contours = detector.detect_objects(img)

        for cnt in contours:

            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect

            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio

            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(img, [box], True, (255, 0, 0), 2)
            cv2.putText(img, "Genislik {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.putText(img, "Uzunluk {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    cv2.imshow("img1", img)
    key = cv2.waitKey(1)
    if key == 27: 
        break

cap.release()
cv2.destroyAllWindows()