#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <wiringPi.h>
#include <pthread.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>

#define PIN_ARM_PWM 2
#define PIN_HAND_PWM 4
#define PIN_MANIPULATOR_ROTATION_PWM 6
#define PIN_MANIPULATOR_PWM 9
#define PIN_STEPS 10
#define PIN_DIR 8



// Struktura reprezentująca dane w pliku
struct PWM_stepper {
    int width_arm;
    int width_hand;
    int width_manipulator_rotation;
    int width_manipulator;
    int do_step;
    int direction;
    int step_speed;

};

struct PWM_stepper data; 

void read_python_data() {
    // Otwórz plik
    while(1){
        sleep(0.2);
    // w trybie binarnym do odczytu  
        FILE *file = fopen("/home/orangepi/Desktop/PWM_and_stepper_data.bin", "rb");
        if (file != NULL) {
                    // int* data  ;                                                   
        size_t bytesRead = fread(&data, sizeof(struct PWM_stepper), 1, file);
        // printf("%lu\n", bytesRead);
        // if(bytesRead == 1)
        // {
           printf("%u , %u , %u, %u, %u, %u, %u \n", data.width_arm, data.width_hand, data.width_manipulator_rotation, data.width_manipulator, data.do_step, data.direction, data.step_speed);

            }


        // }

        fclose(file);
    }
    }


void *thread_arm_PWM(void *arg)
{
    while(1){
        digitalWrite(PIN_ARM_PWM, HIGH);
        delayMicroseconds(data.width_arm);
        digitalWrite(PIN_ARM_PWM, LOW);
        delayMicroseconds(20000 - data.width_arm);
    }
    pthread_exit(NULL);
}
void *thread_hand_PWM(void *arg)
{
    while(1){
        digitalWrite(PIN_HAND_PWM, HIGH);
        delayMicroseconds(data.width_hand);
        digitalWrite(PIN_HAND_PWM, LOW);
        delayMicroseconds(20000 - data.width_hand);
    }
    pthread_exit(NULL);
}
void *thread_manipulator_rotation_PWM(void *arg)
{
    while(1){
        digitalWrite(PIN_MANIPULATOR_ROTATION_PWM, HIGH);
        delayMicroseconds(data.width_manipulator_rotation);
        digitalWrite(PIN_MANIPULATOR_ROTATION_PWM, LOW);
        delayMicroseconds(20000 - data.width_manipulator_rotation);
    }
    pthread_exit(NULL);
}
void *thread_manipulator_PWM(void *arg)
{
    while(1){
        digitalWrite(PIN_MANIPULATOR_PWM, HIGH);
        delayMicroseconds(data.width_manipulator);
        digitalWrite(PIN_MANIPULATOR_PWM, LOW);
        delayMicroseconds(20000 - data.width_manipulator);
    }
    pthread_exit(NULL);
}
void *thread_stepper(void *arg)
{
    while(1){
        if(data.direction){
            digitalWrite(PIN_DIR,HIGH);
        }
        else{
            digitalWrite(PIN_DIR,LOW);
        }
        if(data.do_step){
            digitalWrite(PIN_STEPS,HIGH);
            delayMicroseconds(data.step_speed);
            digitalWrite(PIN_STEPS,LOW);
            delayMicroseconds(data.step_speed);
        }
        else{
        digitalWrite(PIN_DIR,LOW);
        }
    }
    pthread_exit(NULL);
}

void *thread_memory_access(void *arg)
{
    read_python_data();
    pthread_exit(NULL);
}

int main(){
    if(wiringPiSetup()==-1){
        return 1;
    }
    pinMode(PIN_ARM_PWM, OUTPUT);
    pinMode(PIN_HAND_PWM, OUTPUT);
    pinMode(PIN_MANIPULATOR_PWM, OUTPUT);
    pinMode(PIN_MANIPULATOR_ROTATION_PWM, OUTPUT);
    pinMode(PIN_STEPS, OUTPUT);
    pinMode(PIN_DIR, OUTPUT);
    digitalWrite(PIN_STEPS,LOW);
    printf("sterowanie wlaczone");

    pthread_t Arm,Hand,Manipulator,Manipulator_rotation,Stepper,python_communication;         

    if(pthread_create(&Arm,NULL,thread_arm_PWM,NULL) != 0){
        perror("Blad tworzenia watku arm");
        exit(EXIT_FAILURE);
    }

    if(pthread_create(&Hand,NULL,thread_hand_PWM,NULL) != 0){
        perror("Blad tworzenia watku hand");
        exit(EXIT_FAILURE);
    }

    if(pthread_create(&Manipulator_rotation,NULL,thread_manipulator_rotation_PWM,NULL) != 0){
        perror("Blad tworzenia watku manipulator_rotation");
        exit(EXIT_FAILURE);
    }

    if(pthread_create(&Manipulator,NULL,thread_manipulator_PWM,NULL) != 0){
        perror("Blad tworzenia watku manipulator");
        exit(EXIT_FAILURE);
    }

    if(pthread_create(&Stepper,NULL,thread_stepper,NULL) != 0){
        perror("Blad tworzenia watku stepper");
        exit(EXIT_FAILURE);
    }

    if(pthread_create(&python_communication,NULL,thread_memory_access,NULL) != 0){
        perror("Blad tworzenia watku stepper");
        exit(EXIT_FAILURE);
    }


    pthread_join(Arm, NULL);
    pthread_join(Hand, NULL);
    pthread_join(Manipulator_rotation, NULL);
    pthread_join(Manipulator, NULL);
    pthread_join(Stepper, NULL);
    pthread_join(python_communication, NULL);


    // free(thread_arm_PWM);
    // free(thread_hand_PWM);
    // free(thread_manipulator_rotation_PWM);
    // free(thread_manipulator_PWM);
    // free(thread_stepper);
    // free(thread_memory_access);

    return 0;
}