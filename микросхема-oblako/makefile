project.hex: project
	avr-objcopy -O ihex project project.hex
	
project:
	avr-gcc -std=gnu99 -mmcu=atmega8 -ffunction-sections -fdata-sections -Wl,-gc-sections -O2 -o project main.c

write:
	avrdude -c arduino-ft232r -pm8 -v -v  -b 115200 -U flash:w:project.hex
	#sudo avrdude -c duemilanove -pm16 -F -P /dev/ttyUSB0 -B 115200 -U flash:w:project.hex
	#sudo avrdude -c dasa3 -pm8 -F -P /dev/ttyS0 -U flash:w:project.hex
clean:
	./clean.sh
	#rm project project.hex
all: clean project.hex write

fuse:
	#sudo avrdude -c dasa3 -pm8 -F -P /dev/ttyS0 -U lfuse:w:0xff:m -U hfuse:w:0xc9:m
	sudo avrdude -c arduino-ft232r -pm8 -v -v  -b 9600 -U lfuse:w:0x3f:m -U hfuse:w:0xc1:m
