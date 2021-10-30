import board
import neopixel
from time import sleep
import datetime


board.D18
pixel_pin = board.D18
num_pixels = 64
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=.2, auto_write=False, pixel_order=ORDER
)

def night_mode(time):
    if time >=19 and time <24:
        pixels[time-19]=pixels[time-18]=(50,50,50)
        pixels.show()
    elif time >=0 and time <7:
        pixels[time+5]=pixels[time+6]=(50,50,50)
        pixels.show()
    else:
        print("Error with night time")

def rgb_lights(r,g,b):
    pixels.fill((r,g,b))
    pixels.show()

def getMode():
    with open("messages.log", 'r') as readFile:
       mode = readFile.read()
       mode = str(mode.strip())
    print("User set mode as: ", mode)
    return mode;


def set_lighting(mode='normal',time='off'):
    rgb_lights(0,0,0)

    if mode == 'normal':
        t = datetime.datetime.now()
        hr_now = int(t.hour)

        if hr_now >=7 and hr_now <11:
           #morning
           rgb_lights(255,191,0)

        elif hr_now >=11 and hr_now <15:
            #midday
            rgb_lights(255,255,255)

        elif hr_now >=15 and hr_now <19:
            #afternoon
            rgb_lights(204,255,255)

        elif (hr_now >=19 and hr_now <24 or hr_now <=0 and hr_now <7):
            night_mode(hr_now)

    if mode == 'morning':
        rgb_lights(255,191,0)

    if mode == 'midday':
        rgb_lights(255,255,255)

    if mode == 'afternoon':
        rgb_lights(204,155,255)

    if mode == 'off':
        rgb_lights(0,0,0)

    if mode == 'night':
        if time == "off":
            time = 19
        elif not time >=19 and time <24 or not time >= 0 and time <7:
            time = 19
        night_mode(time)



