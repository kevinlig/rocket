# based on https://github.com/jfurcean/pyportal-app-launcher

import time
import board
import adafruit_touchscreen
from adafruit_pyportal import PyPortal

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]

def sendMsg(col, row):
    print(">>_", col, row, "_<<", sep="")

#Initialize the Pyportal with the default_bg set to the BMP file with all your icons.
pyportal = PyPortal(url='',
    json_path='',
    status_neopixel=board.NEOPIXEL,
    default_bg=cwd+"/grid.bmp",
    text_font=cwd+"/fonts/SourceSansPro-SemiBold-17.bdf",
    text_position=((100, 129), (155, 180)),
    text_color=(0x000000, 0x000000),
    caption_text='',
    caption_font=cwd+"/fonts/SourceSansPro-SemiBold-17.bdf",
    caption_position=(40, 220),
    caption_color=0x000000)

# These pins are used as both analog and digital! XL, XR and YU must be analog
# and digital capable. YD just need to be digital
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
    board.TOUCH_YD, board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(320, 240))

p_list = []
while True :

    # If the keyboard is active then we can use the PyPortal like a keyboard (USB HID)
    p = ts.touch_point
    if p:

        # append each touch connection to a list
        # I had an issue with the first touch detected not being accurate
        p_list.append(p)

        #affter three trouch detections have occured. 
        if len(p_list) == 3:

            #discard the first touch detection and average the other two get the x,y of the touch
            x = (p_list[1][0]+p_list[2][0])/2
            y = (p_list[1][1]+p_list[2][1])/2
            

            # I will refer the the icon/button matrix using the following grid.
            # A1 is the icon/button in the top left corner looking at the PyPortal
            # D3 is the icon/button in the bottom right corner
            # +---+----+----+----+----+
            # |   | A  | B  | C  | D  |
            # +---+----+----+----+----+
            # | 1 | A1 | B1 | C1 | D1 |
            # | 2 | A2 | B2 | C2 | D2 |
            # | 3 | A3 | B3 | C3 | D3 |
            # +---+----+----+----+----+

            # For each button/icon pressed we send a keyboard command using kbd.send
            # this can send multiple key presses as if you were pressing them all at the same time
            # I use a mac and have configured each one of my shortcuts to open an application 
            # using ALT+Control+Shift+Command+[some letter] 
            # These shortcuts trigger an application to launch that was configured using Automator 

            # Column A
            col = "A"
            if x > 22.5 and x < 72.5:
                col = "A"
            # Column B
            elif x > 97.5 and x < 147.5:
                col = "B"
            # Column C
            elif x > 172.5 and x < 222.5:
                col = "C"
            # Column D 
            elif x > 247.5 and x < 297.5:
                col = "D"

            # Row 1
            if y > 25 and y < 75:
                sendMsg(col, "1")
            # Row 2
            elif y > 100 and y < 150:
                sendMsg(col, "2")
            # Row 3  
            elif y > 175 and y < 225:
                sendMsg(col, "3")

            # clear list for next detection
            p_list = []

            # sleap to avoid pressing two buttons on accident
            time.sleep(.5)
