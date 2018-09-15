#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import cv2

video = cv2.VideoCapture(0)

ret, bg = video.read()
cv2.imwrite('bg.jpg', bg)

video.release()
