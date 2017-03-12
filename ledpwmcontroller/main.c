//Версия 2.0 управляется бинарной строкой

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
char bufer[14], k=0;//переменные кривого кольцевого буфера
unsigned char pwm[12]={1,1,1,0,0,0,0,0,0,0,0,0};
unsigned char tcnt0;
ISR(USART_RXC_vect){
	unsigned char rxbyte = UDR;
//кольцевой буфер нужен чтобы исключить возможность переполнения из за
//неверных команд через uart
//байты пишуться в закольцованный массив
//при получении 0xff массив обрабатывается
	bufer[k]=rxbyte;//пишем в кольцевой буфер
	k++;
	if(k>=13) k=0;
	if(rxbyte==0xff) set_pwm();//ждём 0xff
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
	cli();
	PORTC=0;//пробую исправить вспышки некстати
	PORTB=0;//Идея была удачной, теперь не моргает:)
	//Это вторая часть кольцевого буфера
	unsigned char u;
	char temp[12], l=0;//сортируем буфер по старшенству
	for(unsigned char j=k;j<12;j++) temp[l++]=bufer[j];
	for(unsigned char j=0;j<k;j++) temp[l++]=bufer[j];
	for (unsigned char i=0;i<12;i++)pwm[i]=temp[i];
	//А теперь затираем буфер на всяк случай.
	//for(unsigned char j=0; j<13;j++) bufer[j]=' ';
	k=0;
	sei();
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
		c>>=1;
		if (pwm[i]) b|=(1<<5);
		if (pwm[i+6]) c|=(1<<5);
		//printf("%i, i=%i\r\n", pwm[i], i);
		}
	PORTB=b;
	PORTC=c;
	tcnt0=1;//это чтоб значение 0 не выпадало!
	TCNT0=0;//сброс таймера на всяк случай
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
	TCCR0=(0<<CS12)|(1<<CS11)|(1<<CS10);//настраиваем делитель /64
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
	//static unsigned char tcnt0;
	//unsigned char b=0, c=0;
	while(1){
	//сбрасываем шим по таймеру
	//Лишняя работа нам не нужна! пусть проверяет лишь один раз.
		if (tcnt0!=TCNT0){
			tcnt0=TCNT0;
			TCCR0=0;//останавливаем таймер
			for(unsigned char i=0;i<6;i++){
				if(tcnt0==pwm[i]) PORTB&=~(1<<i);
				if(tcnt0==pwm[i+6]) PORTC&=~(1<<i);
			}
			TCCR0=(0<<CS12)|(1<<CS11)|(1<<CS10);
			//настраиваем делитель /64
		}
	}
	return 0;
	}
