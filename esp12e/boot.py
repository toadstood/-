#Функция индикации мигает красным диодом или светит зелёным
def error_code(code):
	import time
	import machine
	sid1=machine.Pin(12, machine.Pin.OUT)
	sid2=machine.Pin(13, machine.Pin.OUT)
	if not code: #если code=0 то зажигаем зелёный
		sid2.high()
		return
	else: #если code=0 то зажигаем зелёный
		sid2.low()
		for i in range(5):
			for j in range(code):
				sid1.high()
				time.sleep(0.3)
				sid1.low()
				time.sleep(0.4)
			time.sleep(1)
#функция ищет известные сети и подключается к первой найденой
def do_connect():
    import network
    import webrepl
    #список известных сетей в формате [(b'SSID',b'PASS'),...]
    SP = [(b'OBLAKO', b'NOT_A_PASSWORD_ACTUALLY'),\
     (b'CANDIDUM-HOME', b'NOT_A_PASSWORD_ACTUALLY'),\
     (b'CANDIDUM', b'NOT_A_PASSWORD_ACTUALLY'), (b'MGTS_GPON_9231', b'NOT_A_PASSWORD_ACTUALLY'),\
     (b'TRYPTAMINE', b'NOT_A_PASSWORD_ACTUALLY')]
    ssid=666
    #настройка интерфейса
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    LIST=sta_if.scan() #поиск точек доступа
    
    for i in range(len(SP)): #ищем известные в найденых
        for j in range(len(LIST)):
            if SP[i][0] in LIST[j]:
                ssid=i
                print(SP[i][0],i,j)
                break
        if ssid!=666: break #Нашли
    
    if ssid!=666: #рапортуем об успехе
        print('connecting to network ', SP[ssid])
        sta_if.active(True)
        sta_if.connect(SP[ssid][0], SP[ssid][1])#Подключаемся
        while not sta_if.isconnected():
            pass #ждём подключения и выводим параметры сети
        print('Network configuration:', sta_if.ifconfig())
        webrepl.start() #отладочный интерфейс
        error_code(0) #рапартуем о подключении
    else:#Если нет известной сети
		print('Network not found!')
		error_code(5)

def new_ssid(SSID, PASS):#отладочная функция подключения к сети
    import network
    import webrepl
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    
    if not sta_if.isconnected():
        print('connecting to network ', SSID)
        sta_if.active(True)
        sta_if.connect(SSID, PASS)
        while not sta_if.isconnected():
            pass
        print('Network configuration:', sta_if.ifconfig())
        webrepl.start()
        error_code(0)
	
#Функция отправки команды на сервер
def send_cmd(data):
    import usocket
    SERVER='192.168.150.1'#Адрес и порт прописаны жёстко
    PORT=9090
    s=usocket.socket()
    try:
        s.connect((SERVER,PORT))
        s.send(data)
        #out=s.recv(128)
        s.close()
        #return out
    except OSError:#в случае отсутствия сервера
        print("Connection error")
        error_code(1)
    
        
do_connect() #Подключаемся к сети
