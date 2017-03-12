#!/bin/python
#Очень сырой скрипт
from time import sleep
import random
import math
from serial import *
global ki
#import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
ser = Serial("/dev/ttyUSB0" , 115200)
temp=bytearray(b'test')

RGBsamples = [[219, 240, 37], [254, 190, 0], [254, 74, 0],\
 [192, 0, 240], [142, 47, 240], [178, 210, 0],\
  [138, 139, 47], [219, 0, 240], [0, 244, 244], [254,0,0], [254, 75,0] ]
def path():
    choosedcolours = random.sample(RGBsamples, 4) 
    #случайный выбор 3х клевых цветов из списка
    RGB0 = choosedcolours[0] # для цветных вспышек
    RGB1 = choosedcolours[1] # старт цветового пути
    RGB2 = choosedcolours[2] # промежуточная точка цветового пути
    RGB3 = choosedcolours[3] # конец цветового пути
    tmax=1000
    tseqences = [0, 0.25*tmax, 0.5*tmax, tmax] 
    #временные точки для аппроксимации цветового пути
    rgb_path = [RGB0, RGB1, RGB2, RGB3] # цветовой путь
    r_path = [] # индивидуальные пути
    g_path = []
    b_path = []
    for i in range(len(rgb_path)):
        r_path.append(rgb_path[i][0])
        g_path.append(rgb_path[i][1])
        b_path.append(rgb_path[i][2])

    iR = interpolate.interp1d(tseqences, r_path)
    iG = interpolate.interp1d(tseqences, g_path)
    iB = interpolate.interp1d(tseqences, b_path)


    print(len(tseqences),len(r_path))
    print(len(rgb_path))

#def light():
    for i in range(tmax+1):
        r=iR(i)
        g=iG(i)
        b=iB(i)
        sleep(0.01)
        data=bytearray([int(r),int(g),int(b),int(r),int(g),\
                      int(b),0,0,0,0,0,0,0xff])
        global temp
        if data != temp:
            ser.write(data)
            temp=data
            
    ser.write(bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0xff]))

path()
