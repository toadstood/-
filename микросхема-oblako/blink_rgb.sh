#!/bin/bash
stty 115200 -F /dev/ttyUSB0 -raw -echo
while [ true ]
do
for i in 0 10 25 100 254 100 25 0;
	do echo " 0 0 $i 0 $i 0 0 0 0 " > /dev/ttyUSB0; sleep 0.01;
	done
for i in 0 10 25 100 254 100 25 0;
	do echo " 0 $i 0 $i 0 0 0 0 0 " > /dev/ttyUSB0; sleep 0.01;
	done
for i in 0 10 25 100 254 100 25 0;
	do echo " $i 0 0 0 0 $i 0 0 0 " > /dev/ttyUSB0; sleep 0.01;
	done
for i in 0 10 25 100 254 100 25 0;
	do echo " $i $i $i 0 0 0 $i 0 0 " > /dev/ttyUSB0; sleep 0.01;
	done
for i in 0 10 25 100 254 100 25 0;
	do echo " 0 0 0 $i $i $i $i 0 0 " > /dev/ttyUSB0; sleep 0.01;
	done
sleep 0.5

done
