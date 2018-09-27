# -*- coding: utf-8 -*-
import pyaudio

pa = pyaudio.PyAudio()

c = pa.get_device_count()

for i in range(0,c):
  print("Device index %d :" % i)
  print(pa.get_device_info_by_index(i))