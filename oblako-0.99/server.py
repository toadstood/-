#!/usr/bin/python
# -*- coding: utf-8 -*-
#Тут тоже всё просто, поднимаем сервер, слушаем порт
#Реагируем на команды
import socket
import os
import sys
import test
from time import sleep
#Настройка порта
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
if sys.argv[1]:
	folder=sys.argv[1]
	print(folder)
else:
	folder="/home/alarm/oblako/" #Жестко заданная дириктория скрипта!
#Задавать полный путь важно для корректной работы service юнита
#server.service
while True:
	conn, addr = sock.accept()
	print ('connected:', addr)
	while True:
		data = conn.recv(1024)
		os.system(folder+"kill.sh "+folder)
		if not data:
			break
		if b"grom" in data:
			print("выполнена команда grom мигаем пару раз шумим")
			os.system(folder+"analyse-2.0.py "+folder+"17-1.wav &")
			conn.send(b'ok')
		if b"flash" in data:
			print("выполнена команда flash")
			test.flash(254,1)
			conn.send(b'ok')
		if b"command 3" in data:
			print("выполнена rgb_path_02.py")
			os.system(folder+"rgb_path_02.py &")
			conn.send(b'ok')
		if b"command 4" in data:
			print("выполнена комманда rgb_path_03.py")
			os.system(folder+"rgb_path_03.py &")
			conn.send(b'ok')
		if b"command 5" in data:
			print("выполнена команда 5")
			os.system(folder+"make_it_color.py &")
			conn.send(b'ok')
		#conn.send(data.upper())
	conn.close()
