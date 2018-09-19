# -*- coding: utf-8 -*-
"""
@description: show the sound in decibel
"""
import pyaudio
import numpy as np
import pylab
import time
import struct
import math

RATE = 16000
CHUNK = int(RATE/20) # RATE/number of updates per second

def sound_plot(stream):
    t1 = time.time() # time starting
    data = np.fromstring(stream.read(CHUNK),dtype = np.int16)
    pylab.plot(data)
    pylab.title(i)
    pylab.grid()
    pylab.axis([0,len(data),-2**8,2**8])
    pylab.savefig("sound.png",dpi=50)
    pylab.show(block = False)
    time.sleep(0.5)
    pylab.close('all')
    #print("took %.2f ms." % (time.time() - t1)*1000)
    
def rms(data):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count)
    
def decibel(data):
    return 20 * math.log10( rms(data) )

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,channels = 1,rate = RATE,
                    input = True,frames_per_buffer = CHUNK,input_device_index=4)
    #for i in range(int(20*RATE/CHUNK)):
    while True:
        # for 10 seconds
        #sound_plot(stream)
        data = stream.read(CHUNK)
        r = rms(data)
        de = decibel(data)
        de = de + 94.0
        print("RMS %.2f" % r)
        print("Decibel %d " % int(de))
    stream.stop_stream()
    stream.close()
    p.terminate()
