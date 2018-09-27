#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import ctypes as C
import cv2

libmog = C.cdll.LoadLibrary('./libmog2000.so')

#cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def getfg(img):
    (rows, cols) = (img.shape[0], img.shape[1])
    res = np.zeros(dtype=np.uint8, shape=(rows, cols))
    libmog.getfg(img.shape[0], img.shape[1],
                       img.ctypes.data_as(C.POINTER(C.c_ubyte)),
                       res.ctypes.data_as(C.POINTER(C.c_ubyte)))
    return res


def getbg(img):
    (rows, cols) = (img.shape[0], img.shape[1])
    res = np.zeros(dtype=np.uint8, shape=(rows, cols, 3))

    libmog.getbg(rows, cols, res.ctypes.data_as(C.POINTER(C.c_ubyte)))
    return res

count = 0

if __name__ == '__main__':
    c = cv2.VideoCapture(0)
    print("Generating background, Please wait a few seconds ...")
    while 1:
        _, f = c.read()
        fg = getfg(f)
        bg = getbg(f)
        if count < 500:
            count += 1
            continue
        #cv2.imshow('f', f)
        #cv2.imshow('fg', getfg(f))
        #cv2.imshow('window', bg)
        cv2.imwrite('bg.jpg', bg)
        exit(0)
        #if cv2.waitKey(1) == 27:
        #   exit(0)