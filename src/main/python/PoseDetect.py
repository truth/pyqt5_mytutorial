import cv2
import yolov5

import numpy as np
haar_front_face_xml = 'data/haarcascade_frontalface_default.xml'
haar_eye_xml = 'data/haarcascade_eye.xml'


class Detector(object):
    face_cascade = cv2.CascadeClassifier(haar_front_face_xml)
    eye_cascade = cv2.CascadeClassifier(haar_eye_xml)

    def detect(self,frame):
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 人脸检测
        if self.face_cascade is None:
            print("face_cascade is None")
            return
        faces = self.face_cascade.detectMultiScale(gray_img, 1.3, 5)
        for (x, y, w, h) in faces:
            # 在原图像上绘制矩形
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray_img[y:y + h, x:x + w]
            # 眼睛检测
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.03, 5, 0, (40, 40))
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (ex + x, ey + y), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

    def __init__(self):
        self.model = yolov5.load('yolov5s.pt')

    def do_model(self, frame):
        results = self.model(frame)
        return results
