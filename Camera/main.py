import sys
# This is required to import the PiHatMenu library
sys.path.append('./../')
import PiHatMenu as phm
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

camera = PiCamera()

# Get font stats
font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

while 1:
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	
	# Draw instructions
	draw.text(
		(0, oled.height - 2*font.height),
		"Select: save image",
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
		# Save image
		now = datetime.now()
		file = now.strftime("%Y_%m%d_%H%M%S") + ".jpg"
		camera.capture("Camera/" + file)

		# Print filename to screen
		image = Image.new("1", (oled.width, oled.height))
		draw = ImageDraw.Draw(image)
		draw.text(
			(0,0),
			"File saved as:",
			font = font,
			fill = 255
		)

		draw.text(
			(0, font.height + 2),
			file,
			font = font,
			fill = 255
		)

		oled.image(image)
		oled.show()

		time.sleep(2)
	elif buttons.rising['Menu']:
		break

