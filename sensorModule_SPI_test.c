/* 
 * File:   fishv1.c
 * Author: kille
 *
 * Created on April 19, 2021, 1:44 AM
 */

#include <stdio.h>
#include <stdlib.h>




//PIC16F18877 Configuration Bit Settings

//CONFIG 1
#pragma config FEXTOSC = OFF
#pragma config RSTOSC = HFINTPLL
#pragma config CLKOUTEN = OFF
#pragma config CSWEN = ON
#pragma config FCMEN = ON

// CONFIG 2
#pragma config MCLRE = ON
#pragma config PWRTE = OFF
#pragma config LPBOREN = OFF
#pragma config BOREN = OFF
#pragma config BORV = LO
#pragma config ZCD = OFF
#pragma config PPS1WAY = ON
#pragma config STVREN = OFF

// CONFIG 3
#pragma config WDTCPS = WDTCPS_31
#pragma config WDTE = OFF
#pragma config WDTCWS = WDTCWS_7
#pragma config WDTCCS = SC

// CONFIG 4
#pragma config WRT = OFF
#pragma config SCANE = available
#pragma config LVP = OFF

//CONFIG 5
#pragma config CP = OFF
#pragma config CPD = OFF

// END OF CONFIG STATEMENTS
#define _XTAL_FREQ 32000000
#include <xc.h>
#include "SPI_Slave.h"
#include "temp.h"
#include <math.h>

//#include <string.h>


//Commands accepted by program in SPI
#define tmp 0x01 //"Temperature"
#define wL 0x02 //"Water level"
#define amm 0x03 //"Ammonia"
#define pH 0x04 //"pH"


//global parameters, all of them hold the current values
unsigned char temp_result;
unsigned char water_level;
unsigned char water_level2;
unsigned char pH_result;
unsigned char ammonia_result;
char data;
float temp;

//=======================================================================

   unsigned char switch_water(unsigned char water_level){
    
          if (PORTDbits.RD4 == 0){
             
              LATDbits.LATD2 = ~LATDbits.LATD2;
             water_level = 0b01000100;}
           else if (PORTDbits.RD4==1){
              water_level = 0b00111010;}
            return water_level;
   }


void main(void)
{
    //Set up
    ANSELD = 0b00000000;  //RD0 is a digital input
    ANSELA = 0b00000000;
    ANSELB = 0b00000000;
    ANSELC = 0b00000000;
    ADCON1 = 0x0F;
    TRISB = 0; //Clear portb
    PORTB = 0; //All of portb pins are outputs
    TRISDbits.TRISD2 = 0;
    TRISDbits.TRISD1 = 0;
    TRISDbits.TRISD4 = 1;
    TRISDbits.TRISD0 = 1;
   

    
    SPI_Init_Slave();
   
    //Dummy data that was used during testing
    temp_result = 90;    //good tmp (heater off) = 78-100, bad tmp (heater on) = 0-77
    water_level2 = 58;    //good wL = 58, bad wL = 68
    ammonia_result = 45;        
    pH_result = 45;  
 
    
    while(1)
    {  
      //data = spi_data(0b11001100);
       //water_level2 = switch_water(water_level);
       //temp = OneWireTemp();       
       //temp_result = temp*9/5 + 32; //Convert to F
       
       data = spi_data(temp_result);
       data = spi_data(water_level2);
       data = spi_data(ammonia_result);
       data = spi_data(pH_result);
        
        
     }
}