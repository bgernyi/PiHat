import sys
# This is required to import the PiHatMenu library
sys.path.append('./../')
import PiHatMenu as phm
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def SetServoAngle( angle, pwm, pin ):
	# The duty cycle range is 1-2ms over a 20ms period. This is a duty cylce of 5-10%
	# The input angle range is 0 to 180 degrees
	duty = 2 + (angle * (10/180))
	pwm.ChangeDutyCycle(duty)
	time.sleep(0.3)
	pwm.ChangeDutyCycle(0)
	

buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

# Get previously stored angle
f = open('Servo Motor/state', 'r')
store = f.read()
f.close()
ang = int(store[:-1])

# Set up GPIO PIN for servo motor. No need to set up buttons as these are done in the main menu code
servo_pin = 17 #GPIO017
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50) # 50 Hz

pwm.start(0)

# Get font stats
font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

while 1:
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)

	# Draw servo state information
	draw.text(
		(0,0),
		"Servo Angle: " + str(ang),
		font = font,
		fill = 255
	)
	
	# Draw instructions
	draw.text(
		(0, oled.height - 2*font.height),
		"Left/Right: angle",
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
	if buttons.rising['Left']:
		ang = ang - 45
		if ang > 180:
			ang = 0
		elif ang < 0:
			ang = 180
		SetServoAngle(ang, pwm, servo_pin)
	elif buttons.rising['Right']:
		ang = ang + 45
		if ang > 180:
			ang = 0
		elif ang < 0:
			ang = 180
		SetServoAngle(ang, pwm, servo_pin)
	elif buttons.rising['Menu']:
		break


f = open('Servo Motor/state', 'w')
f.write(str(ang) + '\n')
f.close()
