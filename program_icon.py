import pygetwindow as gw
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import configparser
from graph import show_all_res

def on_exit(icon, item):
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    conf['DEFAULT']['stop program'] = '1'
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)

    icon.stop()


def graph(icon, item):
    pass
    show_all_res()



def main():
    menu = (
        item('show graph', graph),
        item('Exit', on_exit),
    )

    image = Image.open('icon.png')
    icon = pystray.Icon("name", image, menu=menu, title='Count Time')
    icon.run()


if __name__ == '__main__':
    main()
