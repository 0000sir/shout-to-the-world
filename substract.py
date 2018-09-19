#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import cv2
import numpy as np

bg = cv2.imread('bg.jpg')

video = cv2.VideoCapture(0)
history = 30
bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)  # 背景减除器，设置阴影检测
#bs = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=1, detectShadows=True)
bs.setHistory(history)
frames = 0

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = video.read()

    if not ret:
        break

    fg_mask = bs.apply(frame)
    fg_mask = cv2.GaussianBlur(fg_mask, (5,5), 0)

    if frames < history:
        frames += 1
        continue

    #th = cv2.threshold(fg_mask.copy(), 200, 255, cv2.THRESH_BINARY)[1]
    #th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5)), iterations=2)
    #dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5)), iterations=2)
    th = cv2.threshold(fg_mask.copy(), 0, 255, cv2.THRESH_TRIANGLE)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    #image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bg1 = cv2.imread('bg.jpg')

    output = cv2.bitwise_and(frame, frame, mask = closed)
    mask_inv = cv2.bitwise_not(closed)
    output_bg = cv2.bitwise_and(bg1, bg1, mask=mask_inv)
    output = cv2.add(output, output_bg)
    #for i in range(0, len(contours)):
    #    c = contours[i]
    #    x, y, w, h = cv2.boundingRect(c)
        #area = cv2.contourArea(c)
        #if area > 400:
            #cv2.drawContours(frame,contours,i,(0,0,255),3)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #bg1[y:y+h, x:x+w] = frame[y:y+h, x:x+w]
            #bg1 = cv2.bitwise_and(blured, frame, th)

    cv2.imshow('window', output)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
