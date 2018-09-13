import numpy as np
import cv2

cap = cv2.VideoCapture(1)

while(True):
  ret, frame = cap.read()
  cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  cv2.imshow('Camera', frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindow()