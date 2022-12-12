# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:05:04 2022

@author: Philaxer and Boner
"""

import pyaudio
import numpy
import matplotlib.pyplot as plt

FORMAT = pyaudio.paInt16
SAMPLEFREQ = 44100
FRAMESIZE = 1024
NOFFRAMES = 220
p = pyaudio.PyAudio()
print('running')

stream = p.open(format=FORMAT,channels=1,rate=SAMPLEFREQ,
                input=True,frames_per_buffer=FRAMESIZE)
data = stream.read(NOFFRAMES*FRAMESIZE)
decoded = numpy.fromstring(data, 'Int16');

stream.stop_stream()
stream.close()
p.terminate()
# loadeddecoded = numpy.load('Hallo.npy')
print('done')

decoded = decoded[2000:]

for i in range(len(decoded)):
    if decoded[i] > 500:
        decoded = decoded[i:]
        break
    
if len(decoded) >= SAMPLEFREQ:
    decoded = decoded [:SAMPLEFREQ]

while(len(decoded) < SAMPLEFREQ):
    decoded = numpy.append(decoded, 0)
    
print(decoded)
print(len(decoded))

numpy.save('MRechts5', decoded)
plt.plot(decoded)
plt.show()
