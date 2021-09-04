/* 
 * File:   temp.h
 * 
 *
 * Created on April 19, 2021, 10:51 AM
 */

#ifndef TEMP_H
#define	TEMP_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <xc.h>

//Config to make PIC in open drain
#define BUSDIR LATDbits.LATD0  //set as input or output
#define BUSOUT TRISDbits.TRISD0 //set output high or low
#define BUSIN PORTDbits.RD0 // read input

#define _XTAL_FREQ 32000000

//Available functions from temp library
float OneWireTemp(void); //Returns temperature in celsius
unsigned int OneWireReset(void); //Sends a reset pulse to the sensor
void OneWireWriteBit(unsigned char); //write a single bit to the OneWire
unsigned char OneWireReadBit(void); //reads a single bit
void OneWireWriteByte(unsigned char); //writes a byte
unsigned char OneWireReadByte(void); //reads a byte
unsigned char OneWireRead(void); //reads the current status of the bus
void OneWireHigh(void); //sets the bus high
void OneWireRelease(void); //Releases the bus


#endif	/* TEMP_H */

