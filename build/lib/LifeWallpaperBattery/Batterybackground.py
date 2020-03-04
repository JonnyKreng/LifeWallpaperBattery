#!/usr/bin/env python

import psutil
import screeninfo
import os
import time
from PIL import Image, ImageFilter
import config

def batttery_level():
    battery = psutil.sensors_battery()
    return battery.power_plugged, round(battery.percent)

def get_screen_size():
    screens = screeninfo.get_monitors()
    if(len(screens) == 0):
        raise Exception('No screens found!') 
    for x in screens:
        if(config.name == x.name):
            return (x.width, x.height)
    return screens[0].width, screens[0].height

def battery_image(path):
    image = Image.open(path)
    image = image.resize((int(image.width*config.size),int(image.height*config.size)))
    return image

def background_image(path = ''):
    if(path == ''):
        image = Image.new('RGBA', get_screen_size())
    else:
        image = Image.open(path)
        image = image.convert("RGBA")
    return image

def combine_images(background, battery):
    image = background.copy()
    mask = battery.split()[3].point(lambda i: i > config.maskfilter and 255)
    image.paste(battery, (int((background.width / 2) - (battery.width / 2)),int((background.height / 2) - (battery.height / 2))), mask)
    return image

def process_battery(battery, powerlevel):
    image = battery.copy()
    if(config.unsimingly):
        multiR = int(255 - (255 * (powerlevel[1]/100)))
        multiG = int((200 * (powerlevel[1]/100)))
        nulltpl = (0,0,0,0)
        for x in range(image.width):
            for y in range(image.height):
                point = image.getpixel((x,y))
                if(point[3] == 0):
                    image.putpixel((x,y), nulltpl)
                else:
                    image.putpixel((x,y),(multiR, multiG, 0, point[3]))
    else:
        color = config.colorlist[0][1]
        for a in config.colorlist:
            if(a[0] >= powerlevel[1]):
                color = a[1]
        nulltpl = (0,0,0,0)
        for x in range(image.width):
            for y in range(image.height):
                point = image.getpixel((x,y))
                if(point[3] == 0):
                    image.putpixel((x,y), nulltpl)
                else:
                    image.putpixel((x,y), color)


    top = image.height-image.height*(powerlevel[1]/100)
    mask = image.crop((0,top, image.width, image.height))
    battery.paste(mask, (0, battery.height-mask.height))

    return battery 

def set_wallpaper(path):
    os.system("""    
    dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
    var Desktops = desktops();                                                                                                                       
    for (i=0;i<Desktops.length;i++) {
            d = Desktops[i];
            d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper",
                                        "org.kde.image",
                                        "General");
            d.writeConfig("Image", "file://"""+ os.path.abspath(path) +"""");
    }'
    """)

def main():
    back = background_image(config.background)
    batt = battery_image(config.battery)
    while(True):              
        image = combine_images(back, process_battery(batt, batttery_level()))
        image.save(config.outputpath)
        set_wallpaper(config.outputpath)
        time.sleep(config.frametime)

main()