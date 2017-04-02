#!/bin/bash
#слкрипт убивающий выполняемые световые эфекты
#не самая лучшая реализация в плане избыточности, но
#должно быть надёжно
DIR=$1 #адрес целевых скриптов.
cd $DIR
echo `pwd`.
killall aplay
for i in *.py
do #убиваем всё кроме server.py
    [ $i != "server.py" ] && killall $i 2>/dev/null
    echo $i is killed
done 
