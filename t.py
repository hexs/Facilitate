import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

class Icon(pystray.Icon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_menu(self):
        super().update_menu()


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

def f_visible(icon, item):
    icon.visible = False

def main():
    menu = (
        item('Exit', on_exit),
        item('p1', f_visible)
    )

    image = create_image()
    icon = Icon("name", image, menu=menu)
    icon.run()

if __name__ == '__main__':
    main()
