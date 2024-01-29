import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

def create_image():
    width, height, color1, color2 = 64, 64, 'black', 'white'
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

def on_exit(icon, item):
    icon.stop()

# Create a menu with a single item (Exit)
menu = (item('Exit', on_exit),)

# Create an image for the tray icon
image = create_image()

# Create a PyStray icon without specifying a backend
icon = pystray.Icon("name", image, menu=menu)

# Run the icon in the system tray
icon.run()
