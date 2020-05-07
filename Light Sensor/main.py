import sys
# This is required to import the PiHatMenu library
sys.path.append('./../')
import PiHatMenu as phm
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import smbus, time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

# Get font stats
font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

# Setup Light Sensor parameters
# Code adapted from Matt at raspberrypi-spy.co.uk
DEVICE = 0x23	# Sensor address
MODE = 0x13	# High resolution one-time measurement 
bus = smbus.SMBus(1)

def readLight(bus, addr, mode):
	# Read data from I2C interface
	data = bus.read_i2c_block_data(addr,mode)
	result = (data[1] + (256* data[0])) / 1.2
	return result

while 1:
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)

	# Draw fan state information
	draw.text(
		(0,0),
		"Measurement (in Lx):",
		font = font,
		fill = 255
	)

	# Get light level measurement
	lightLvl = readLight(bus, DEVICE, MODE)
	
	# Draw instructions
	draw.text(
		(0, oled.height - 2*font.height),
		str(format(lightLvl, '.2f')) + " Lx",
		font = font,
		fill = 255
	)
	draw.text(
		(0, oled.height - font.height),
		"Menu: go back",
		font = font,
		fill = 255
	)

	# Fill screen
	oled.image(image)
	oled.show()

	# Update buttons detection
	buttons.update()

	# Set according changes
	if buttons.rising['Menu']:
		break
