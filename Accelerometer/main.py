import sys
# This is required to import the PiHatMenu library
sys.path.append('./../')
import PiHatMenu as phm
from PIL import Image, ImageDraw, ImageFont
import smbus2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

# Setup accelerometer
addr = 0x0A
bus = smbus2.SMBus(1)

def readAccData(addr, bus):
    offset = 4 # data offset as specified by the BMA220 datasheet
    data = bus.read_i2c_block_data(addr, offset, 3)

    # Apply 2's compliment to data
    for i in range(0,3):
        if data[i] > 127:
            data[i] = (-1)*(255 + 1 - data[i])
        # Convert to g-force (max of +- 8g)
        data[i] = data[i]*2/128

    return data
    

# Get font stats
font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

while 1:
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)

	# get accelerometer measurement
	acc = readAccData(addr, bus)

        # Draw data to OLED
	draw.text(
                (0,0),
                "X:" + str(format(acc[0], '.3f')) + "g, Y:" + str(format(acc[1], '.3f')) + "g",
                font = font,
                fill = 255
        )
	draw.text(
		(0, oled.height - 2*font.height),
		"Z:" + str(format(acc[2], '.3f')) + "g",
#                "X: " + str(format(int(acc[0]*128/8), '03d')) + ', ' + str(format(int(acc[0]*128/8), '#08b')),
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
