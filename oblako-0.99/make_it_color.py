#!/bin/python
#скрипт включает опредёлённый цвет из набора классных
import sys
import random
from serial import *
ser = Serial("/dev/ttyUSB0" , 115200)
#набор классных цветов
RGBsamples = [[219, 240, 37], [254, 190, 0], [254, 74, 0],\
 [192, 0, 240], [142, 47, 240], [178, 210, 0], [138, 139, 47],\
  [219, 0, 240], [0, 244, 244]]
color = random.sample(RGBsamples, 1)*3
out=[]
for i in color:
	for j in i:
		out.append(int(j))
ser.write(bytearray(out+[0,0,0xff]))
