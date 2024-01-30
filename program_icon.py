import json
import time

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from func import req_dict


class Icon(pystray.Icon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_menu(self):
        super().update_menu()
        print('update_menu')
        if self.visible:
            with open('data_program.json') as f:
                data = json.loads(f.read())
            data['show_ui'] = not data['show_ui']
            with open('data_program.json', 'w') as f:
                f.write(json.dumps(data))


def create_image():
    width, height, color1, color2 = 64, 64, 'black', 'white'
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
    req_dict('write?close program=True')
    icon.stop()


def f_visible(icon, item):
   pass


def main():
    menu = (
        item('p1', f_visible),
        item('Exit', on_exit),
    )

    image = create_image()
    icon = Icon("name", image, menu=menu, title='-')
    icon.run()


if __name__ == '__main__':
    main()
