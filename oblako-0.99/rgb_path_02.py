#!/bin/python
#Цветовые переходы через заданные цвета, промодулированные
#Заданной функцией
from time import sleep
import random
import math
from serial import *
global ki
#import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
ser = Serial("/dev/ttyUSB0" , 115200)

RGBsamples = [[219, 240, 37], [254, 190, 0], [254, 74, 0],\
 [192, 0, 240], [142, 47, 240], [178, 210, 0], [138, 139, 47],\
  [219, 0, 240], [0, 244, 244], [254,0,0], [254, 75,0] ]
def path():
    choosedcolours = random.sample(RGBsamples, 4)
     #случайный выбор 3х клевых цветов из списка
    RGB0 = choosedcolours[0] # для цветных вспышек
    RGB1 = choosedcolours[1] # старт цветового пути
    RGB2 = choosedcolours[2] # промежуточная точка цветового пути
    RGB3 = choosedcolours[3] # конец цветового пути
    global tmax
    tmax=100
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
    #выводим отладочные данные

    print(len(tseqences),len(r_path))
    print(len(rgb_path))

    for i in range(tmax+1):
        r=iR(i)
        g=iG(i)
        b=iB(i)
        r1=r*(math.sin(i/3.14)+1)/2
        g1=g*(math.sin(i/3.14)+1)/2
        b1=b*(math.sin(i/3.14)+1)/2
        r2=r*(math.cos(i/3.14)+1)/2
        g2=g*(math.cos(i/3.14)+1)/2
        b2=b*(math.cos(i/3.14)+1)/2
        b2=b*(math.cos(i/3.14)+1)/2
        b2=b*(math.cos(i/3.14)+1)/2
        sleep(0.3)
        ser.write(bytearray([int(r1),int(g1),int(b1),\
                     int(r2),int(g2),int(b2),0,0,0,0,0,0,0xff]))
        #ser.write(bytearray([r,g,b,r,g,b,0,0,0,0,0,0,0xff]))

path()

