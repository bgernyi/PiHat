import PiHatMenu as phm
from PIL import Image, ImageDraw, ImageFont

menu = phm.createmenu()
buttons = phm.Input_Buttons(phm.pins, phm.labels, 3)
oled = phm.setupoled()

font = ImageFont.load_default()
(font.width, font.height) = font.getsize('aaaaa')

halfway = (oled.height/2) - (font.height/2)

# Clear screen
oled.fill(0)
oled.show()

selection=0
while 1:
        # Create new image for screen
	image = Image.new("1", (oled.width, oled.height))
	draw = ImageDraw.Draw(image)

        # Draw selection arrow
	draw.line(
                xy = [(0, oled.height/2 - 3), (10, oled.height/2), (0, oled.height/2 + 3)],
                fill = 255,
                width=2
        )
        
        # Draw each option
	for x in range(selection - 1,selection + 2):
		(font.width, font.height) = font.getsize(menu[x % len(menu)].name)
		draw.text(
			(15,(halfway+ 1)+ (x - selection)*font.height),
			menu[x % len(menu)].name,
			font = font,
			fill = 255
		)

	oled.image(image)
	oled.show()

	# The buttons.update function must be run every loop to ensure debouncing
	buttons.update()

	# Button detection, and appropriate actions to take
	if buttons.rising['Up']:
		selection = selection - 1
	elif buttons.rising['Down']:
		selection = selection + 1
	elif buttons.rising['Select']:
		# Open the specified option in the same scope as this program
		menu[selection].run()

#	print(selection)
	selection = selection % len(menu)
