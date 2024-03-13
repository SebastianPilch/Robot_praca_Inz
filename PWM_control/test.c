// #include "pca9685.c"
// #include <wiringPi.h>


// #include <stdio.h>
// #include <stdlib.h>

// #define PIN_BASE 300
// #define MAX_PWM 4096
// #define HERTZ 50


// /**
//  * Calculate the number of ticks the signal should be high for the required amount of time
//  */
// int calcTicks(float impulseMs, int hertz)
// {
// 	float cycleMs = 1000.0f / hertz;
// 	return (int)(MAX_PWM * impulseMs / cycleMs + 0.5f);
// }

// /**
//  * input is [0..1]
//  * output is [min..max]
//  */
// float map(float input, float min, float max)
// {
// 	return (input * max) + (1 - input) * min;
// }


// int main(void)
// {
// 	printf("PCA9685 servo example\n");
// 	printf("Connect a servo to any pin. It will rotate to random angles\n");
// 	// Calling wiringPi setup first.
// 	    if(wiringPiSetup()==-1){
//         return 1;
//     }
// 	// // Setup with pinbase 300 and i2c location 0x40

// 	printf("cokolwiek");
// 	int fd = pca9685Setup(PIN_BASE, 0x40, HERTZ);
// 	if (fd < 0)
// 	{
// 		printf("Error in setup\n");
// 		return fd;
// 	}

// 	// Reset all output
// 	pca9685PWMReset(fd);


// 	// Set servo to neutral position at 1.5 milliseconds
// 	// (View http://en.wikipedia.org/wiki/Servo_control#Pulse_duration)
// 	float millis = 1.5;
// 	int tick = calcTicks(millis, HERTZ);
// 	pca9685PWMWrite(fd,0,0, tick);
// 	delay(2000);


// 	int active = 1;
// 	while (active)
// 	{
// 		// That's a hack. We need a random number < 1
// 		float r = rand();
// 		while (r > 1)
// 			r /= 10;

// 		millis = map(r, 1, 2);
// 		tick = calcTicks(millis, HERTZ);
// 		printf("cokolwiek");
// 		pca9685PWMWrite(fd,4,100,2000);
// 		delay(1000);
// 	}

// 	return 0;
// }


#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <wiringPi.h>
#include <pthread.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>

// #define PCA9685_ADDR 0x40

// #define MODE1 0x00
// #define MODE2 0x01
// #define PRE_SCALE 0xFE
// #define LED0_ON_L 0x06

// void initPCA9685(int fd){

// 	wiringPiI2CWriteReg8(fd,MODE1,0x20);
// 	wiringPiI2CWriteReg8(fd,PRE_SCALE,0x79);
// 	wiringPiI2CWriteReg8(fd,MODE1,0x21);

// }

// void setPWM(int fd, int channel,int on, int off){

// 	int baseReg = LED0_ON_L +4*channel;
// 	wiringPiI2CWriteReg8(fd,baseReg,on & 0xFF);
// 	wiringPiI2CWriteReg8(fd,baseReg+1,on >>8);
// 	wiringPiI2CWriteReg8(fd,baseReg+2,off & 0xFF);
// 	wiringPiI2CWriteReg8(fd,baseReg+3,off >>8);
// }

// int main(){



// wiringPiSetup();
// int fd = wiringPiI2CSetup(PCA9685_ADDR);
// if(fd ==-1){
// 	printf("Nie poczono");
// 	return 1;
// }
// printf("%d", fd);
// initPCA9685(fd);
// int offValue = 500;
// for(int i=0;i<10;i++){
// int channel = 7;
// int onValue = 0;

// setPWM(fd,channel,onValue,offValue);
// delay(1000);
// offValue = offValue + 400;
// }
// return 0;

// }
#define PIN_SDA 0
#define PIN_SCL 1



void start_i2c()
{
	digitalWrite(PIN_SCL, HIGH);
	digitalWrite(PIN_SDA,LOW);
	delayMicroseconds(4);
}

int sendAddres_Write()
{
	digitalWrite(PIN_SCL, HIGH);
	digitalWrite(PIN_SDA,LOW);

	digitalWrite(PIN_SDA,LOW);

	return 0;
}



int send8bits(int data)
{	
	if(data <0)
	{	
		data = 0;
	}
	if(data > 0xFFF){
		data = 0xFFF;
	}
	start_i2c();


	digitalWrite(PIN_SDA,HIGH);


	return 0;
}



int main()
{
wiringPiSetup();
// pinMode(PIN_SDA,OUTPUT);
// pullUpDnControl(PIN_SDA,PUD_UP);
// // pinMode(PIN_SCL,OUTPUT);
// pullUpDnControl(PIN_SCL,PUD_UP);
digitalWrite(PIN_SCL,HIGH);
digitalWrite(PIN_SDA,HIGH);


return 0;
}
