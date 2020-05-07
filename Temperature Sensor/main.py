import sys
# This is required to import the PiHatMenu library
sys.path.append('./../')
import PiHatMenu as phm
from PIL import Image, ImageDraw, ImageFont
import smbus, time, os, glob
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

# Code adapted from circuitbasics.com
# Setup the one-wire interface for the temp sensor
os.system('modprobe w1-gpio')
os.system('modprope w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def readTempCelcius(file_dir):
	f = open(file_dir, 'r')
	lines = f.readlines()
	f.close()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.1)
		lines.readTempRaw(file_dir)
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_str = lines[1][equals_pos+2:]
		return float(temp_str)/1000.0

# Get font stats
font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

temp = readTempCelcius(device_file)

while 1:
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)

	# Draw fan state information
	draw.text(
		(0,0),
		str(format(temp, '.3f')) + " C",
		font = font,
		fill = 255
	)

	# Get light level measurement
	#temp = readTempCelcius(device_file)
	
	# Draw instructions
	draw.text(
		(0, oled.height - 2*font.height),
		"Down: Update temperature",
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
	elif buttons.rising['Down']:
                temp = readTempCelcius(device_file)
