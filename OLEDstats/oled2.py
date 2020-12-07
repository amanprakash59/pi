# Script to display System info on 128x64 i2c oled display 
# Script Modified from original Adafruit_Python_SSD1306 Library
# Modified by AmanPrakash659 for Pi4
import psutil
import time
import subprocess as sp
#import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used


# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)



# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()



font2 = ImageFont.truetype('ap.ttf', 16)
font_icon = ImageFont.truetype('fontawesome-webfont.ttf', 16)




while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

### Icons
    # Icon Wifi
    draw.text((x, top+1), chr(61598),  font=font_icon, fill=255)
    # Icon temperator
    #draw.text((x+80, top+16),    chr(62152),  font=font_icon1, fill=255)
    # Icon sd
    #draw.text((x+3, top+3), chr(61952),  font=font_icon, fill=255)
 
 
###CPU USAGES
    cpu_usage = sp.getoutput('vcgencmd measure_clock arm')

    buff=cpu_usage[14:17]
    buff=int(buff)
    buffg=cpu_usage[14:15]
    buffm=cpu_usage[15:16]
    if ( buff < 500 ):
        cpu_usage = buffg+ "." + buffm + " GHz"
    else:
        buff = str(buff)
        cpu_usage = buff + " MHz"
### GPU USAGES
 
    gpu_usage = sp.getoutput('vcgencmd measure_clock v3d')
    buff=gpu_usage[14:17]
    buff=int(buff)
    buffg=gpu_usage[14:15]
    buffm=gpu_usage[15:16]
    if ( buff < 200 ):
        gpu_usage = buffg+ "." + buffm + " GHz"
    else:
        buff = str(buff)
        gpu_usage = buff + " MHz"
       
### DISK SPACE 
    hdd = psutil.disk_usage('/')
    def get_total_space():
        return hdd.total / (2**30)
    def get_used_space():
        return hdd.used / (2**30)
    def get_free_space():
        return hdd.free / (2**30)
    

    total = str(round(get_total_space(), 2))
    used = str(round(get_used_space(), 2))
    free = str(round(get_free_space(),2))
 
   #print ("Total: " + total)
   # print ("Used: " + used)
   # print ("Free: " + free)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = sp.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = sp.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"MEM: %s/%s MB %.0f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = sp.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = sp.check_output(cmd, shell = True )

    # Coode To print stuffs on oled
    
 
    draw.text((x+20, top), "AmAn's Pi  B+ ", font=font2, fill=255)
 #   draw.text((x, top+9), " Owner : AmAn PraKasH ", font=font, fill=255)
    draw.text((x, top+8), "______________________________", font=font, fill=255)
    draw.text((x, top+19), "CPU: " + cpu_usage +" | "+str(temp,'utf-8'),font = font,fill=225)
    draw.text((x, top+28), "GPU: "+ gpu_usage, font=font, fill=255)
    draw.text((x, top+37),str(MemUsage,'utf-8'), font=font, fill=255)
    draw.text((x, top+46), "SD : "+used+"/"+total+" GB", font=font, fill=255)
    draw.text((x, top+55),"IP : " +str(IP,'utf-8'), font=font, fill=255)
#-------------------------------------------------------

    # Display image.
    
    disp.image(image)
    disp.display()
    time.sleep(.1)