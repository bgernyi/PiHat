import sys
# This is required to import the PiHatMenu library
sys.path.append('./../')
import PiHatMenu as phm
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import alsaaudio, wave, os
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

# Get font stats
font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

# File name of recording
f_name = 'recording.wav'

def play(device, f):
	import alsaaudio
	print('%d channels, %d sampling rate\n' % (f.getnchannels(), f.getframerate()))
	
	# Set attributes
	device.setchannels(f.getnchannels())
	device.setrate(f.getframerate())

#    # 8bit is unsigned in wav files
#    if f.getsampwidth() == 1:
#        device.setformat(alsaaudio.PCM_FORMAT_U8)
#    # Otherwise we assume signed data, little endian
#    elif f.getsampwidth() == 2:
	device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
#    elif f.getsampwidth() == 3:
#        device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
#    elif f.getsampwidth() == 4:
#        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
#    else:
#        raise ValueError('Unsupported format')

	periodsize = 160
	device.setperiodsize(periodsize)
	
	data = f.readframes(periodsize)
	while data:
		# Read data from stdin
		device.write(data)
		data = f.readframes(periodsize)

device = alsaaudio.PCM(device="default")

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 44100 Hz, 16 bit little endian samples
inp.setchannels(2)
inp.setrate(44100)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

while 1:
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)
	
	# Draw instructions
	draw.text(
		(0, oled.height - 2*font.height),
		"Select: record/playback",
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

		os.remove(f_name)
		# Alert user of audio recording
		image = Image.new("1", (oled.width, oled.height))
		draw = ImageDraw.Draw(image)
		draw.text(
			(0,0),
			"Recording audio...",
			font = font,
			fill = 255
		)
		oled.image(image)
		oled.show()

		f = wave.open(f_name, 'wb')
		f.setnchannels(2)
		f.setsampwidth(2)
		f.setframerate(44100)
		# Record for a few seconds
		loops = 100000
		while loops > 0:
			loops -= 1
			l, data = inp.read()

			if l:
				f.writeframes(data)
				time.sleep(.001)

		f.close()

		# Alert user that audio is being played back
		image = Image.new("1", (oled.width, oled.height))
		draw = ImageDraw.Draw(image)
		draw.text(
			(0,0),
			"Playing back...",
			font = font,
			fill = 255
		)
		oled.image(image)
		oled.show()
		# Play back recorded audio
		f = wave.open(f_name, 'rb')
		play(device, f)

		f.close()

	elif buttons.rising['Menu']:
		break

