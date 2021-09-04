from time import sleep
from signal import pause
from gpiozero import LED
import spidev
import alert
from website import webDisplay

def spiCom(module, data, device):
    sleep(3)
    print("\n"+module+" request")
    #Slave select Power Module
    if device == 0:
        sensorMod.on()
        powerMod.off()
    #Slave select Sensor Module
    if device == 1:
        powerMod.on()
        sensorMod.off()
    inData = spi.xfer2(data)
    #if device == 1:
     #   print("\nEnter Temperature: ")
      #  inData[0] = int(input())
       # print("\nEnter Water Level: ")
     #   inData[1] = int(input())
      #  print("\nEnter Ammonia: ")
       # inData[2] = int(input())
       # print("\nEnter pH: ")
        #inData[3] = int(input())
    if device == 0:
        print("\nEnter Power Status: ")
        inData[0]= 33
        #inData[0] = int(input())
        #print("\nEnter Battery Level: ")
        #inData[1] = int(input())
        inData[1]= 98
    powerMod.on()
    sensorMod.on()
    return inData



#Setup SPI
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000
spi.mode = 0

#Settup GPIO pins
powerMod = LED(24)
sensorMod = LED(26)

#Variables
tmp = 0
wL = 0
amm = 0
pH = 0

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
    msg.append(amm)
    msg.append(wL)
    msg.append(pH)
    result1 = spiCom(var1, msg, 1)

    #check power module results
    if result0[0] == 43:   #Battery is on!
        tmp_wL = 42    #Turn off heater and water filler tmp_wL = 42
        battery_lvl_status = result0[1]    #get batter percentage
        heater = 89    #heater must be off
        filler = 77    #water filler must be off
    else:   #Battery is off
        battery_lvl_status = 99
        tmp_wL = 32
        #Check Sensor Module results
        if int(result1[0]) <78:  #Turn on the heater
            heater = 99
        else:
            heater = 89
        if result1[1] == 78:    #Water level is too low! Turn on water filler
            filler = 87
        else:
            filler = 77

    tmp = result1[0]
    wL = result1[1]
    amm = result1[2]
    pH = result1[3]
    power_status = result0[0]

    webDisplay(result1[0], result1[1], result1[2], result1[3])


    if power_status == 43:
        alert.send_email()
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
    sleep(10)


