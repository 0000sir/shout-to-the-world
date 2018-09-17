#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import cv2

video = cv2.VideoCapture(0)
history = 30
bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
bs.setHistory(history)
frames = 0

while True:
    ret, frame = video.read()

    if frames < history:
        frames += 1
        continue

    fg_mask = bs.apply(frame)
    fg_mask = cv2.GaussianBlur(fg_mask, (5,5), 0)
    bg_mask = cv2.bitwise_not(fg_mask)
    th = cv2.threshold(bg_mask.copy(), 255, 0, cv2.THRESH_TRIANGLE)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    bg = cv2.bitwise_and(frame, frame, mask = bg_mask)

    cv2.imshow('bg', bg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
