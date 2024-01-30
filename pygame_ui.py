import json
import os
import time
from datetime import datetime
import pygame
import requests
from func import req, req_dict

def ui(data):
    while True:
        time.sleep(0.2)
        dic_data = req_dict('api')
        if dic_data.get('close program'):
            break
        if dic_data.get('show ui'):
            x = 1920 - 300
            y = 1080 - 400 - 48
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x}, {y}"
            pygame.init()
            screen = pygame.display.set_mode((300, 400))

            clock = pygame.time.Clock()
            running = True

            while running:
                dic_data = req_dict('api')
                if dic_data.get('show ui') == False:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        req('write?show ui=False')

                screen.fill("purple")
                pygame.display.flip()
                clock.tick(60)
            pygame.quit()


if __name__ == '__main__':
    print('ui ok')
    data = {'run program': True}
    ui(data)
