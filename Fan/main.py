import sys
# This is required to import the PiHatMenu library
sys.path.append('./../')
import PiHatMenu as phm
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

# Set up GPIO PIN for fan. No need to set up buttons as these are done in the main menu code
fan_pin = 13
GPIO.setup(fan_pin, GPIO.OUT)

# Get previously stored state
f = open('Fan/state', 'r')
store = f.read()[0]
f.close()

# Get font stats
font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

if store == '1':
	state = True
	state_str = "on"
else:
	state = False
	state_str = "off"

# Set fan to initial state
GPIO.output(fan_pin, state)

while 1:
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)

	# Draw fan state information
	draw.text(
		(0,0),
		"Fan: " + state_str,
		font = font,
		fill = 255
	)
	
	# Draw instructions
	draw.text(
		(0, oled.height - 2*font.height),
		"Select: fan on/off",
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
	if buttons.rising['Select']:
		state = not state
		GPIO.output(fan_pin, state)
	elif buttons.rising['Menu']:
		break

	if state:
		state_str = "on"
	else:
		state_str = "off"


f = open('Fan/state', 'w')
if state:
	f.write("1\n")
else:
	f.write("0\n")

f.close()
