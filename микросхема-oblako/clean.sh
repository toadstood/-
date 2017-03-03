#!/bin/bash
for i in project project.hex
do
	if [ -f $i ] 
		then
		rm $i
	fi
done
