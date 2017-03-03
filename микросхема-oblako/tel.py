#!/bin/python
from serial import *
from tkinter import *
import threading
import os
import re
import tkinter.messagebox
flag=True


if os.path.exists("/dev/ttyUSB0"):
	serialPort = "/dev/ttyUSB0"
	baudRate = 115200
	ser = Serial(serialPort , baudRate) #ensure non-blocking
else:
	tkinter.messagebox.showinfo("ERROR", "\"/dev/ttyUSB0\" не найден")
	quiet();

	

def ser_w(s):
	ser.write(bytes(s,encoding="utf-8"))

def readSerial():
    global flag
    while True:
      c = ser.readline()
      c=str(c.decode('utf-8'))
      if "RING" in c :
        if flag: os.system("mplayer music/Undervud/2005\ -\ Бабло\ побеждает\ зло/01\ -\ Бабло\ победит\ зло.mp3 1>/dev/null 2>&1 &")
        flag=False
      if "ATH" in c:
        if not flag: os.system("killall mplayer 2>/dev/null")
      if len(c) > 2:
        log.insert('end', c.replace("\r",""))
        log.see("end")

#make a TkInter Window
root = Tk()
root.wm_title("My telephone")

# make a text box to put the serial output
log = Text ( root, width=40, height=10, takefocus=0)
log.grid(row=0,column=0,sticky='ns')

# make a scrollbar
scrollbar = Scrollbar(root)
scrollbar.grid(row=0,column=1,sticky='ns')

# attach text box to scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)


button2=Button(root,width=25, height=1,font="arial 14",text="Принять звонок")
button2.grid(row=1,column=0,columnspan=2)
button2.bind("<Button-1>", lambda _: ser_w("ATA\r\n"))

button1=Button(root,width=25, height=1,font="arial 14",text="Отклонить звонок")
button1.grid(row=2,column=0,columnspan=2)
button1.bind("<Button-1>", lambda _: ser_w("ATH\r\n"))

#entry1=Entry(root,width=36)
#entry1.grid(row=3,column=0,columnspan=2)

#button3=Button(root,width=25, height=1,font="arial 14",text="test")
#button3.grid(row=4,column=0,columnspan=2)
#button3.bind("<Button-1>", lambda _: ser_w("AT\r\n"))

entry2=Entry(root,width=37,bd=3)
entry2.grid(row=5,column=0,columnspan=2)

def send_command(root):
	
	s=entry2.get()+"\r\n"
	entry2.delete(0, END)
	ser.write(bytes(s,encoding="utf-8"))
entry2.bind("<Return>", send_command)
entry2.focus()
      
t=threading.Thread(target=readSerial)
t.setDaemon(True)
t.start()
root.mainloop()
