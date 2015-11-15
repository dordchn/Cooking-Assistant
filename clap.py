#!/usr/bin/env python

import os
import sys
import wave
import pyaudio
import audioop
from ctypes import *

def listenAndCount(duration): # record(2, "output.wav")
	CHUNK = 256 # 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = duration
	THRESHOLD=7000

	###### SUPRESS pyaudio alsa errors
	ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
	def py_error_handler(filename, line, function, err, fmt):
		return
	c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
	asound = cdll.LoadLibrary('libasound.so.2')
	asound.snd_lib_error_set_handler(c_error_handler)
	#############

	p = pyaudio.PyAudio() # Throwing annoying and irrelevant errors

	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)

	#print("* recording")

	loud=False
	counter=0

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		mx = audioop.max(data, 2)
		if (mx>THRESHOLD): # if quiet
			if (loud==False): # if wasn't quiet till now
				counter+=1
				loud=True
		else:
			loud=False

	#print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	return counter

def waitForClaps():
	count=listenAndCount(3)
	while (count==0):
		count=listenAndCount(3)
	return count

######################################################################

if __name__ == '__main__':
	if (len(sys.argv)!=2):
		print "Usage: ./clap.py <time (s)>\n"
		sys.exit(0)
	print "Claps: " + str(listenAndCount(int(sys.argv[1])));