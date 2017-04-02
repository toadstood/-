import random
import math
from time import sleep
from serial import *
ser = Serial("/dev/ttyUSB0" , 115200)

def flash(a,t):
	b=random.uniform(0.03, t)
	i=0
	c=1
	if a>254: a=254
	while c:
		c=int(a*math.exp(-b*i))
		i+=1
		print(c)
		sleep(0.02)
		ser.write(bytearray([c,c,c,0,0,0,0,0,0,0,0,0,0xff]))

flash(254,0.5)
