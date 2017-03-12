#!/bin/python
#Собственно ради этого скрипта всё и затевалось
#Скрипт анализирует waw файл, после чего воспроизводит его
#Сопровождая амплитудозависимой модуляцией 
import os
import sys
import random
from time import sleep
import wave
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
import math
from serial import *
ser = Serial("/dev/ttyUSB0" , 115200)#Настройка порта
inputfile=sys.argv[1]
#открываем файл, считываем информацию, о файле
wav = wave.open(inputfile, mode="r") 
(nchannels, sampwidth, framerate, nframes,\
              comptype, compname) = wav.getparams()
#считаем продолжительность в секундах
duration = nframes / framerate
#К имеет такое значение чтоб весь файл поместился в массив из 1000
#точек
k = int(nframes/3000)
#Считываем данные из файла, преобразуем в массив, считая что файл 16битный
content = wav.readframes(nframes)
samples = np.fromstring(content, dtype=np.int16)

#делаем выборку из массива 1000 точек из одного канала (оттуда и двойка)
channel = samples[1::2*k]
#берём модуль от массива
channel=np.abs(channel)
#отсекаем тихие звуки
m=np.max(channel)*0.13
print(m)
for i in range(channel.size):
	if channel[i]<m:
		channel[i]=0
	if channel[i]>25000:
		channel[i]=25000
	#else: 
		#if channel[i]: channel[i]+=1000
def f(a):
	#задаём рандомный цвет xyz, почему именно так,
	# потому что яркость постоянна
	d=[[]]
	out=[]
	for i in range(3):
		x=random.uniform(0, 1)
		y=random.uniform(0, 1-x)
		z=1-x-y
		d.append([x,y,z])
	if a>254: a=254
	for i in d:
		for j in i:
			out.append(int(j*a))
	
	#m задаёт режим вывода.
	if a>150:#7,8,9 каналы включаются при a>150
		ser.write(bytearray(out+[0,0,0xff]))
		return
	if a>50:#аналогично 3,4,5
		ser.write(bytearray(out[:6]+[0,0,0,0,0,0xff]))
		return
	ser.write(bytearray(out[:3]+[0,0,0,0,0,0,0,0,0,0xff]))

#Определяем паузу между посылками
pause=duration/channel.size-0.001
print(pause)
#считаем коэфицыэнт пересчёта интенсивности
m=254/np.max(channel)
delay=int(0.3/pause)

def wf():
	for i in range(channel.size):
		#запускаем воспроизведение в заданное время.
		if i==delay: os.system("aplay -q "+inputfile+" &")
		if channel[i]!=channel[i-1]:#передаём только если значения новые!!!
			#меняем выход
			f(channel[i]*m)#выводим данные на канал out
		sleep(pause)#ждём
	ser.write(bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0xff]))#тушим свет
#plt.plot(range(channel.size),channel)
#name=inputfile+".png"
#plt.savefig(name, dpi=300)
#plt.show()
wf() #Поехали

