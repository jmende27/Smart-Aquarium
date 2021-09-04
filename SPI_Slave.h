/* 
 * File:   SPI_Slave.h
 * 
 *
 * Created on April 19, 2021, 11:29 AM
 */

#ifndef SPI_SLAVE_H
#define	SPI_SLAVE_H
#include <xc.h>
#include <stdlib.h>


//unsigned char data;

void SPI_Init_Slave();
unsigned char spi_data(unsigned char dummy);


void SPI_Init_Slave(){
    RC5PPS = 0x15;
    SSP1CLKPPS = 0x13;
    SSP1DATPPS = 0x14; 
    //SSP1SSPPS = 0x03;// this would have set ss to RA3, not RA5.
    SSP1SSPPS = 0x05;
    //SSP1CON1 = 0b00100100;
    SSP1CON1bits.CKP=0;//clock polarity = 0
    SSP1CON1bits.SSPM=0b0100;
    SSP1STAT = 0b00000000;
    SSP1STATbits.CKE = 1;
    SSP1CON1bits.SSPEN = 1;
    
    //SSP1STAT = 0b00000000;
    SSP1STATbits.CKE = 1;
    ADCON1 = 0x0F; 
    TRISCbits.TRISC3 = 1;  // Clock //SCLK
    TRISCbits.TRISC4 = 1;  //Serial data input // MOSI
    TRISCbits.TRISC5 = 0;  //output data// MISO
    TRISAbits.TRISA5 = 1;  //Client Select Input //SS
  
}


unsigned char spi_data(unsigned char dummy){ 
    char Data;
    SSP1BUF = dummy;
    PIR3bits.SSP1IF=0;
    while(SSP1STATbits.BF==0)
        ;
    while(PIR3bits.SSP1IF==0)
        ; 
     LATDbits.LATD1 = ~LATDbits.LATD1;
     Data=SSP1BUF; 
     PIR3bits.SSP1IF=0;
    return Data;
}

#endif	/* SPI_SLAVE_H */

