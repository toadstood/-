#Ну тут всё просто, ждём нажатия кнопок и отсылаем команды
import machine
import time
#Настройка кнопок
p14=machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
p5=machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
p2=machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
p0=machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
p4=machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
#Обработка нажатий
while True:
	if not p14.value():
		while not p14.value():#Ждём отпускания кнопки
			pass
		send_cmd('flash')#Посылаем команду
		print("flash")#рапортуем
		#Функция send_cmd() прописана в boot.py
	if not p2.value():
		while not p2.value():
			pass 
		send_cmd('grom')
		print("grom")
		
	if not p0.value():
		while not p0.value():
			pass 
		send_cmd('command 3')
		print("command 3")
		
	if not p4.value(): 
		while not p4.value():
			pass
		send_cmd('command 4')
		print("command 4")
		
	if not p5.value(): 
		while not p5.value():
			pass
		send_cmd('command 5')
		print("command 5")


