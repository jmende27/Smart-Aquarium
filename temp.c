/* 
 * File:   temp.c
 * Author: kille
 *
 * Created on April 19, 2021, 10:51 AM
 */

#include <stdio.h>
#include <stdlib.h>
#include "temp.h"

/* //Available functions
float OneWireTemp(void); //Returns temperature in celsius
unsigned int OneWireReset(void); //Sends a reset pulse to the sensor
void OneWireWriteBit(unsigned char); //write a single bit to the OneWire
unsigned char OneWireReadBit(void); //reads a single bit
void OneWireWriteByte(unsigned char); //writes a byte
unsigned char OneWireReadByte(void); //reads a byte
unsigned char OneWireRead(void); //reads the current status of the bus
void OneWireHigh(void); //sets the bus high
void OneWireRelease(void); //Releases the bus */


//==============================================================
float OneWireTemp(){
    
    OneWireReset();
    OneWireWriteByte(0xCC);
    OneWireWriteByte(0x44);
    //BUSIN = 0;
   while (!BUSIN);
    OneWireReset();
    OneWireWriteByte(0xCC);
    OneWireWriteByte(0xBE); // Read Scratchpad (BEh) - 15 bits
    unsigned char LSB = OneWireReadByte();
    unsigned char MSB = OneWireReadByte();
    OneWireReset(); //stop reading
    
    unsigned int data = MSB;
    float temperature = (data << 8) | LSB;
    return (temperature/16);
}

void OneWireHigh(){
    BUSDIR = 0; //set as output
    BUSOUT = 1; // set high
}

void OneWireRelease(){
    BUSDIR = 0; //set as output
    BUSOUT = 0; //set low
}
unsigned char OneWireRead(){
    return BUSIN;
}

unsigned int OneWireReset(){
    OneWireRelease();
    __delay_us(240);
    __delay_us(240);
    OneWireHigh();
    __delay_us(70);
    unsigned int OW = OneWireRead();
    __delay_us(205);
    __delay_us(205);
    OneWireHigh();
    return OW;
}

void OneWireWriteBit(unsigned char b){
    if(b){
        OneWireRelease();
        __delay_us(6);
        OneWireHigh();
        __delay_us(64);
    }
    else{
        OneWireRelease();
        __delay_us(60);
        OneWireHigh();
        __delay_us(10);
    }
}



unsigned char OneWireReadBit(){
    OneWireRelease();
    __delay_us(6);
    OneWireHigh();
    __delay_us(9);
    unsigned char out = OneWireRead();
    __delay_us(55);
    return out;
}

void OneWireWriteByte(unsigned char b){
    for(int i = 0; i < 8; i++){
        OneWireWriteBit(b & 0x01); //send LS bit first
        b = b >> 1;
    }
}


unsigned char OneWireReadByte(void){
    unsigned char out;
    for(int i = 0; i < 8; i++){
        out = out >> 1;
        if(OneWireReadBit() & 0x01)
            out = out | 0x80;
    }
    return out;
}

