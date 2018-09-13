# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
import pyaudio
import struct
import ft2

RATE = 16000
CHUNK = int(RATE/20)
SWITCH = 60

VIDEO_DEFAULT = "videos/vod1.m4v"
VIDEO_60 = "videos/vod2.m4v"

def volume_of(data):
  count = len(data)/2
  format = "%dh"%(count)
  shorts = struct.unpack(format, data)
  sum_squares = 0.0
  for sample in shorts:
      n = sample * (1.0/32768)
      sum_squares += n*n
  rms = math.sqrt( sum_squares / count)
  decibel = 20 * math.log10( rms )
  return int(decibel+90)

def write_dB(img, volume, max, ft):
  height, width = img.shape[:2]
  if volume>SWITCH:
    text = "%d分贝" % volume
    position = (int(width/2 - 96),int(height*0.1))
  else:
    text = "请开始呐喊"
    position = (int(width/2 - 134),int(height*0.1))
  
  max_text = "最高纪录: %d 分贝" % max
  max_position = (int(width/2 - 200), int(height*0.2))
  img = ft.draw_text(img, position, text , 48, (255,255,255))
  img = ft.draw_text(img, max_position, max_text , 48, (255,255,255))
  return img
  
def mix_with_camera(frame, cap1, cap2):
  ret, avatar1 = cap1.read()
  avatar1 = cv2.resize(avatar1, (320, 240))
  avatar1 = cv2.flip(avatar1, 1)
  ret2, avatar2 = cap2.read()
  avatar2 = cv2.resize(avatar2, (320, 240))
  avatar2 = cv2.flip(avatar2, 1)
  
  height, width = frame.shape[:2]
  frame[0:240, 0:320] = avatar1
  frame[0:240, width-320:width] = avatar2
  return frame
  
if __name__ == '__main__':
  p = pyaudio.PyAudio()
  stream = p.open(format = pyaudio.paInt16,channels = 1,rate = RATE,
                  input = True,frames_per_buffer = CHUNK,input_device_index=2)
  camera1 = cv2.VideoCapture(1) # capture camera
  camera2 = cv2.VideoCapture(2)
  cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  
  video_default = cv2.VideoCapture(VIDEO_DEFAULT)
  video_60 = cv2.VideoCapture(VIDEO_60)
  
  font = cv2.FONT_HERSHEY_SIMPLEX
  fontScale              = 1
  ft = ft2.put_chinese_text('wqy-zenhei.ttc')
  
  max_volume = 0
  
  while(True):
    data = stream.read(CHUNK, exception_on_overflow = False)
    volume = volume_of(data)
    if volume > max_volume:
      max_volume = volume
      print max_volume

    #ret1, avatar = cap.read()
    
    if volume < SWITCH:
      playing_video = video_default
    else:
      playing_video = video_60
    
    ret, frame = playing_video.read()
    if ret==0:
      playing_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
      continue
    
    
    frame = mix_with_camera(frame, camera1, camera2)
    frame = write_dB(frame, volume, max_volume, ft)
    cv2.imshow('Camera', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    
  # clear
  stream.stop_stream()
  stream.close()
  p.terminate()
  video_default.release()
  video_60.release()
  camera1.release()
  camera2.release()
  cv2.destroyAllWindows()
    