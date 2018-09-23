import numpy as np
import ctypes as C
import cv2

libmog = C.cdll.LoadLibrary('./libmog2.so')

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

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


if __name__ == '__main__':
    c = cv2.VideoCapture(0)
    while 1:
        _, f = c.read()
        fg = getfg(f)
        #bg = getbg(f)
        bg = cv2.imread('bg.jpg')
        #cv2.imshow('f', f)
        #cv2.imshow('window', fg)
        #cv2.imshow('window', getbg(f))
        th = cv2.threshold(fg, 0, 255, cv2.THRESH_TRIANGLE)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        output = cv2.bitwise_and(f, f, mask = closed)
        mask_inv = cv2.bitwise_not(closed)
        output_bg = cv2.bitwise_and(bg, bg, mask=mask_inv)
        output = cv2.add(output, output_bg)
        cv2.imshow('window', fg)
        if cv2.waitKey(1) == 27:
            exit(0)
