from time import sleep
import spidev
import alert
import lights
import database
import serverRefresh

def spiCom(module, data, device):
    print("\n"+module+" SPI data transfer.")

    #Slave select Power Module
    if device == 1:
        P_inData = [0,0,0,0,0]
        spi2 = spidev.SpiDev()
        spi2.open(0,1)
        spi2.mode = 0
        spi2.xfer2([5],50000,3000)
        P_inData = spi2.xfer2(data,50000,3000)
        print(P_inData)
        print("SPI power module transfer complete")
        spi2.close()

    #Slave select Sensor Module
    if device == 0:
        S_inData = [0,0,0,0]
        spi = spidev.SpiDev()
        spi.open(0,0)
        spi.mode = 0
        spi.xfer2([5],50000,3000)
        S_inData = spi.xfer2(data,50000,3000)
        print(S_inData)
        print("SPI transfer complete\n")
        spi.close()

    if device == 1:
        return P_inData
    return S_inData




#Variables
tmp = 5
wL = 5
amm = 5
pH = 5
pwr_stat = 5       #battery off = 33, on = 43
btry_lvl = 5       #99 is default for battery off, when on value is percentage of juice left in battery
heater_flag = 5    #heater off is 89, on is 99
filler_flag = 5    #filler off is 77, on is 87
FnH_flag = 5       #emergeny shut off flag for both heater/filler, for both to be off = 42, value = 32 meaning system is normal

var1 = "Power Module"
var0 = "Sensor Module"

# Initiate SPI results with 0
result0 = result1 = 0


inData = [tmp,wL,pwr_stat,btry_lvl];
outData = [heater_flag,filler_flag,FnH_flag];
strData = ["5","5","5","5","5","5","5","5","5"];


while 1:

    #Sending Power Module request
    msg = [pwr_stat]
    msg.append(btry_lvl)
    msg.append(heater_flag)
    msg.append(filler_flag)
    msg.append(FnH_flag)
    result1 = spiCom(var1, msg, 1)

    #Sending Sensor Module request
    msg = [tmp]
    msg.append(wL)
    msg.append(amm)
    msg.append(pH)
    result0 = spiCom(var0, msg, 0)


   #Get data from SPI transactions
    inData[0] = int(result0[0])  #Get temperature
    inData[1] = int(result0[1])  #Get water level
    inData[2] = int(result1[0])  #Get power status
    inData[3] = int(result1[1])  #Get battery level

    #Set output signals and variables if battery is enabled
    if inData[2] == 43:  #Battery is on
        outData[2] = 42  #System flag: emergency shutoff
        outData[0] = 89  #Heater flag: off
        outData[1] = 77  #Filler flag: off
        strData[4] = "Battery Enabled"
        strData[5] = str(inData[3])+"%"
        lights.set_lighting(mode='off')  #Turn off LED's
#        alert.send_notifications()

    #Set output signals and variables if battery is disabled
    elif inData[2] == 33:   #Battery is off
        inData[3] = 100  #Battery level always fully charged
        outData[2] = 32  #system flag: normal
        strData[4] = "Battery Disabled"
        strData[5] = "100%"
        user_command = lights.getMode()  #Get user command for lighting
        lights.set_lighting(mode=user_command)   #Set lighting

        #Check Sensor Module results
        if inData[0] >= 0 and inData[0] < 78:  #Check for cold water
            outData[0] = 99  #turn on heater
        elif inData[0] >= 78 and inData[0] < 100:  #Check for good temp
            outData[0] = 89  #turn off heater
        else:
            outData[0] = 6  #temperature error

        if inData[1] == 68:  #Water level is too low!
            outData[1] = 78  #Turn on water filler
            strData[1] = "Low"
        elif inData[1] == 58:  #Water level is good, turn off the water filler
            outData[1] = 77  #Turn off water filler
            strData[1] = "High"
        else:
            outData[1] = 6  #water level error
            strData[1] = "Error WL"
    else:
        outData[0] = outData[1] = outData[2] = 6  #power status error
        strData[4] = strData[5] = "Error PS"


    tmp = inData[0]
    wL = inData[1]
    amm = int(result0[2])
    pH = int(result0[3])
    pwr_stat = inData[2]
    btry_lvl = inData[3]
    filler_flag = outData[1]
    heater_flag = outData[0]
    FnH_flag = outData[2]

    if amm == 11:
        strData[2] = "alarm"
    elif amm == 22:
        strData[2] = "toxic"
    elif amm == 33:
        strData[2] = "alert"
    elif amm == 44:
        strData[2] = "safe"
    else:
        strData[2] = "undetermined"

    if heater_flag == 89:
        strData[6] = "Heater off"
    elif heater_flag == 99:
        strData[6] = "Heater on"
    else:
        strData[6] = "Error H"

    if filler_flag == 77:
        strData[7] = "Filler off"
    elif filler_flag == 78:
        strData[7] = "Filler on"
    else:
        strData[7] = "Error Filler"

    if FnH_flag == 32:
        strData[8] = "System Normal"
    elif FnH_flag == 42:
        strData[8] = "System Shutoff"
    else:
        strData[8] = "Error Sys"

    strData[0] = str(tmp)
    strData[3] = str(pH)

    database.save_data(strData[0],strData[1],strData[2],strData[3],strData[4],strData[5])
    serverRefresh.refresh()

    print(f"tmp=",strData[0])
    print(f"wL=", strData[1], ": ", wL)
    print(f"amm=", strData[2], ": ", amm)
    print(f"pH=", strData[3])
    print(f"power status=", strData[4], ": ", pwr_stat)
    print(f"battery_lvl=", strData[5], ": ", btry_lvl)
    print(f"heater flag=",strData[6], ": ", heater_flag)
    print(f"filler flag=",strData[7], ": ", filler_flag)
    print(f"tmp_wL flag=",strData[8],": ", FnH_flag)
    sleep(5)


