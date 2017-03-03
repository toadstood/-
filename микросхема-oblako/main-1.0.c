//Версия 1.0 управляется читабельной строкой

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
char bufer[13], k=0;//переменные кривого кольцевого буфера
unsigned char pwm[12]={55,55,60,0,0,0,0,0,0,0,0,0};
//по уму надо замутить структуру или класс, но впадел.
ISR(USART_RXC_vect){
	char rxbyte = UDR;
//кольцевой буфер нужен чтобы исключить возможность переполнения из за
//неверных команд через uart
//байты пишуться в закольцованный массив
//по нажатии return массив обрабатывается
	bufer[k]=rxbyte;//пишем в кольцевой буфер
	k++;
	if(k>=39) k=0;
	if(rxbyte=='\r') set_pwm();//ждём нажатия return
//можно ещё эхо сделать но лень
}
//стандартный ввод-вывод для отладки
/*
void put_char(unsigned char data,FILE *stream){
	while(!(UCSRA&(1<<5)));//ждём готовности
	UDR=data;//отправляем
	//return 0;
	};
	
static unsigned char get_char(FILE *stream){
	while(!(UCSRA&(1<<7)));
	return UDR;
	};

static FILE mystdout=FDEV_SETUP_STREAM(put_char,get_char,_FDEV_SETUP_RW);
*/
void set_pwm(void){
	unsigned char u;
	char temp[39], l=0;//сортируем буфер по старшенству
	for(unsigned char j=k;j<39;j++) temp[l++]=bufer[j];
	for(unsigned char j=0;j<k;j++) temp[l++]=bufer[j];
	//Это вторая цасть кольцевого буфера
	//temp[5]='\n';
	//printf("bufer %s\r\n", temp );
	//справил ошибку сменив j на l++
	PORTC=0;//пробую исправить вспышки некстати
	PORTB=0;//Идея была удачной, теперь не моргает:)
	//Дерьбаним кольцевой буфер на значения ШИМ
	//тут круче чем в прошивке для счёта интервала
	//там был просто scanf, а здесь кольцевой буфер + sscanf!!!
	sscanf(temp,"%u %u %u %u %u %u %u %u %u",&pwm[0],&pwm[1],&pwm[2]\
	,&pwm[3],&pwm[4],&pwm[5],&pwm[6],&pwm[7],&pwm[8]);
	//printf("pwm[0]=%d, pwm[1]=%d, pwm[2]=%d\r\n",pwm[0],pwm[1],pwm[2]);
	//А теперь затираем буфер на всяк случай.
	for(unsigned char j=0; j<39;j++) bufer[j]=' ';
	k=0;
}
//Вывод чисто по приколу;)
void uart_putstr( char *str ){
	while(*str){
		//ждем окончания передачи предыдущего байта
		while( ( UCSRA & ( 1 << UDRE ) ) == 0 );
		UDR = *str++;
		}
}


ISR(TIMER0_OVF_vect){
//включаем пины если в переменных шима не 0;
	unsigned char c=0,b=0;
	for (unsigned char i=0; i<6; i++){
		b>>=1;
		if (pwm[i]!=0) b|=(1<<5);
		//printf("%i, i=%i\r\n", pwm[i], i);
		} 
	for (unsigned char i=6; i<12; i++){
		c>>=1;
		if (pwm[i]) c|=(1<<5);
		//printf("%i, i=%i\r\n", pwm[i],i);
		}
		//printf("b=%i, c=%i\r\n", b,c);
	PORTB=b;
	PORTC=c;
	//
	//printf("b=%d, c=%d\r\n", b,c);
}

int main(void){
	TIMSK|=(1<<TOIE0);//прерывание по переполнению таймера 0
	//настройка скорости обмена 115200 при частоте 11,0592
	UBRRL = 0x5;
	//8 бит данных, 1 стоп бит, без контроля четности
	UCSRC = ( 1 << URSEL ) | ( 1 << UCSZ1 ) | ( 1 << UCSZ0 );
	//разрешить прием, передачу данных и прерывание по приёму байта
	UCSRB = ( 1 << TXEN ) | ( 1 << RXEN ) | (1 << RXCIE );
	TCCR0=(1<<CS12)|(0<<CS11)|(0<<CS10);//настраиваем делитель /256
	//и запускаем timer0
	TCNT0=0;
	uart_putstr("SHAMAN's programm PWM;)\r\n");
	//отладочный вывод
	//stdin=stdout=&mystdout;
	//printf("Hello world!\r\n");
	//настройк портов
	DDRC=0b111111;
	DDRB=0b111111;
	PORTC=0;
	PORTB=0;
	sei();
	//unsigned char b=0, c=0;
	while(1){
	//сбрасываем шим по таймеру
	//тут есть некотрая избыточность
	//тк сбрасывать он один и тот же бит будет не раз
	//уж за 256 тактов он всяко пару раз успеет
		for(unsigned char i=0;i<6;i++){
			if(TCNT0==pwm[i]) PORTB&=~(1<<i);
		}
		for(unsigned char i=6;i<12;i++){
			if(TCNT0==pwm[i]) PORTC&=~(1<<(i-6));
		}
	}
	return 0;
	}
