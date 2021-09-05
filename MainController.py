from time import sleep
#from signal import pause
from gpiozero import LED
import spidev
#import alert
from website import webDisplay

def spiCom(module, data, device):
    print("\n"+module+" SPI data transfer.")

    #Slave select Power Module
    if device == 0:
        P_inData = [0,0,0,0, 0]
        sensorMod.on()
        powerMod.off()

        print("\nPower status: ")
        P_inData[0] = int(input())
        print("\nBattery lvl status: ")
        P_inData[1] = int(input())
        print("\nDummy heater flag: ")
        P_inData[2] = int(input())
        print("\nDummy filler flag: ")
        P_inData[3] = int(input())
        print("\nDummy tmp_wL flag: ")
        P_inData[4] = int(input())

    #Slave select Sensor Module
    if device == 1:
        S_inData = [0,0,0,0]
        powerMod.on()
        sensorMod.off()
        S_inData = spi.xfer2(data)
        print("SPI transfer complete\n")

    powerMod.on()
    sensorMod.on()
    if device == 0:
        return P_inData
    return S_inData



#Setup SPI
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 50000
spi.mode = 0

#Settup GPIO pins
powerMod = LED(26)
sensorMod = LED(24)

#Variables
tmp = 5
wL = 4
amm = 7
pH = 10

power_status  = 33    #battery off = 33, on = 43
battery_lvl_status = 99     #99 is default for battery off, when on value is percentage of juice left in battery
heater = 89    #heater off is 89, on is 99
filler = 77    #filler off is 77, on is 87
tmp_wL = 32    #emergeny shut off flag for both heater/filler, for both to be off = 42, value = 32 meaning system is normal

var0 = "Power Module"
var1 = "Sensor Module"

# Initiate SPI results with 0
result0 = result1 = 0

#Initiate  slave select GPIOs to logic 1 (deselecting  slave devices)
powerMod.on()
sensorMod.on()

while 1:

    #Sending Power Module request
    msg = [power_status]
    msg.append(battery_lvl_status)
    msg.append(tmp)
    msg.append(wL)
    msg.append(tmp_wL)
    result0 = spiCom(var0, msg, 0)

    #Sending Sensor Module request
    msg = [tmp]
    msg.append(wL)
    msg.append(amm)
    msg.append(pH)
    result1 = spiCom(var1, msg, 1)

    #check power module results
    int_powerStatus = int(result0[0])
    if int_powerStatus == 43:   #Battery is on!
        tmp_wL = 42    #Turn off heater and water filler tmp_wL = 42
        battery_lvl_status = result0[1]    #get battery percentage
        heater = 89    #heater must be off
        filler = 77    #water filler must be off
    elif int_powerStatus == 33:   #Battery is off
        battery_lvl_status = 99
        tmp_wL = 32
        #Check Sensor Module results
        int_tmp = int(result1[0])
        if int_tmp >= 0 and int_tmp < 78:  #Turn on the heater
            heater = 99
        elif int_tmp >= 78 and int_tmp < 100: #Turn off the heater
            heater = 89
        else:
            print("tmp signal ERROR!\n")

        int_wL = int(result1[1])
        if int_wL == 68:    #Water level is too low! Turn on water filler
            filler = 78
        elif int_wL == 58:    #Water level is good, turn off the water filler
            filler = 77
        else:
            print("wL signal ERROR!")
    else:
        print("Power Status Signal ERROR\n")
      

    tmp = result1[0]
    wL = result1[1]
    amm = result1[2]
    pH = result1[3]
    power_status = result0[0]

    webDisplay(result1[0], result1[1], result1[2], result1[3])


    if power_status == 43:
        #alert.send_email()
        #alert.send_sms()
       

    print(f"tmp=",tmp)
    print(f"wL=",wL)
    print(f"amm=",amm)
    print(f"pH=",pH)
    print(f"power status=",power_status)
    print(f"battery_lvl=",battery_lvl_status)
    print(f"heater flag=",heater)
    print(f"filler flag=",filler)
    print(f"tmp_wL flag=",tmp_wL)

  


