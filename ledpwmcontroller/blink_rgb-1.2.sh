#!/bin/bash
#простенький скрипт для проверки работы контроллера
stty 115200 -F /dev/ttyUSB0 -raw -echo
while [ true ]
do
for i in 0 1 3 5 10 25 100 254 100 25 10 5 3 1 0;
	do echo -e "\0"0"\0"0"\0"$i"\0"0"\0"$i"\0"0"\0"0"\0\0\0\0\0" > /dev/ttyUSB0;sleep 0.05;
	done
for i in 0 1 3 5 10 25 100 254 100 25 10 5 3 1 0;
	do 	echo -e "\0"0"\0"$i"\0"0"\0"$i"\0"0"\0"0"\0"0"\0\0\0\0\0" > /dev/ttyUSB0;sleep 0.05;
	done
for i in 0 1 3 5 10 25 100 254 100 25 10 5 3 1 0;
	do echo -e "\0"$i"\0"0"\0"0"\0"0"\0"0"\0"$i"\0"0"\0\0\0\0\0" > /dev/ttyUSB0;sleep 0.05;
	done
for i in 0 1 3 5 10 25 100 254 100 25 10 5 3 1 0;
	do echo -e "\0"$i"\0"$i"\0"$i"\0"0"\0"0"\0"0"\0"0"\0\0\0\0\0" > /dev/ttyUSB0; sleep 0.05;
	done
for i in 0 1 3 5 10 25 100 254 100 25 10 5 3 1 0;
	do echo -e "\0"0"\0"0"\0"0"\0"$i"\0"$i"\0"$i"\0"$i"\0\0\0\0\0" > /dev/ttyUSB0; sleep 0.05;
	done
sleep 0.2

done
