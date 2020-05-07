This is a basic piece of software that is setup to run on a PiHit designed by QUT.

The required libraries to run this are:

python3-rpi.gpio

adafruit-circuitpython-ssd1306

python3-pil

smbus (pip3)

libasound2-dev

https://github.com/larsimmisch/pyalsaaudio (git clone)

https://github.com/waveshare/WM8960-Audio-HAT

python3-picamera


For the temperature sensor, add the following line to /boot/config.txt:

dtoverlay=w1-gpio



To run this program, unzip this whole repo, and run MainMenu.py
