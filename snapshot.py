#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import cv2

v = cv2.VideoCapture(0)

_, frame = v.read()

cv2.imwrite('bg.jpg', frame)