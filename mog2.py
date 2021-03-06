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
        #cv2.imshow('f', f)
        #cv2.imshow('fg', getfg(f))
        cv2.imshow('window', getbg(f))
        if cv2.waitKey(1) == 27:
            exit(0)
