import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import os, board, time, threading
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# A class for debouncing individual buttons. Uses a pin number, and number of debouncing bits
class Debouncer():
	def __init__(self, pin, numbits):
		self.pin = pin
		self.state = 0
		self.rising = False
		self.falling = False
		self.bits = numbits

	def read(self):
		cur = GPIO.input(self.pin)
		if (self.state == (2 ** (self.bits-1)) - 1) and (cur == True):
			self.rising = True
		else:
			self.rising = False

		if(self.state == (2 ** self.bits) - 1) and (cur == False):
			self.falling = True
		else:
			self.falling = False

		self.state = self.state << 1
		self.state = self.state & ((2 ** self.bits) - 1)
		if cur:
			self.state = self.state + 1

class Tile():
	def __init__(self, name, rootdir):
		self.name = name
		self.dir = rootdir + "/" + name
		self.runpath = self.dir + '/main.py'
	def run(self):
		exec(open(self.runpath).read())

class Input_Buttons():
	def __init__(self, GPIO_pins, labels, numbits):
		if len(GPIO_pins) != len(labels):
			raise NameError('pins and labels lists must be the same length, and in order')
		self.pins = GPIO_pins
		self.labels = labels
		self.db = list()
		self.rising = {}
		self.falling = {}
		for i in range(0, len(labels)):
			GPIO.setup(GPIO_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			self.db.append(Debouncer(GPIO_pins[i], numbits))

		for i in self.labels:
			self.rising[i] = False
			self.falling[i] = False
	
	def active(self, index):
		return self.labels[i]

	def update(self):
		for i in range(len(labels)):
			self.db[i].read()
			self.rising[labels[i]] = self.db[i].rising
			self.falling[labels[i]] = self.db[i].falling

def createmenu():
	# Create list of main menu options
	rootdir = os.getcwd()
	options = os.listdir()
	options = sorted(options)
	menu = list()
	
	for x in options:
		if os.path.isdir(rootdir + "/" + x):
			if x != '__pycache__':
				menu.append(Tile(x, rootdir))
	return menu

def setupoled():
	# Setup the OLED screen first
	# Screen pixel dimensions
	WIDTH = 128
	HEIGHT = 32
	
	# Setup screen communication using I2C
	i2c = board.I2C()
	return adafruit_ssd1306.SSD1306_I2C(WIDTH,HEIGHT, i2c, addr = 0x3C)


pins = [22, 23, 24, 25, 26, 27] # GPIO.BCM Pins
#pins = [15, 16, 18, 22, 37, 13] # GPIO.BOARD pins
labels = ['Up', 'Down', 'Left', 'Right', 'Menu', 'Select']
