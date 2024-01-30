import os
import time

import win32gui
import win32con
import sys
import ctypes
import pygame
import pygame_gui
import json
from datetime import datetime, timedelta
import configparser
import numpy as np
import pyautogui
import pygetwindow as gw
import re

conf = configparser.ConfigParser()
conf.read('config.ini')


def write_to_config_file():
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)


def update_data_program(data_program):
    old_dt = datetime.now()
    while data_program['play']:
        dt = datetime.now()
        if (dt - old_dt).total_seconds() > 1:
            old_dt = dt
            # 1 sec
            if data_program['close ui']:
                data_program['close ui'] = False
                with open('data_program.json', 'w') as f:
                    f.write(json.dumps({'show_ui': False}, indent=4))
            else:
                with open('data_program.json') as f:
                    string = f.read()
                dic = json.loads(string)
                data_program['show_ui'] = dic['show_ui']


def run(data_program):
    try:
        with open('data.json') as f:
            data = json.loads(f.read())
        time_axis = data['time']
        window_active_axis = data['window_active']
        mouse_moved_axis = data['mouse_moved']
        result_axis = data['result']
    except:
        print('except')
        time_axis = []
        window_active_axis = []
        mouse_moved_axis = []
        result_axis = []

    all_time = len(result_axis)  # เวลาทั้งหมดที่เปิดโปรแกรม
    ac_time = result_axis.count(1)  # เวลาที่ทำงาน
    last_dt_window_active = datetime.now()
    last_dt_mouse_move = datetime.now()
    mouse_pos = pyautogui.position()
    old_dt = datetime.now()
    save_data = False

    while data_program['play']:
        dt = datetime.now()

        # update window_active
        gwget = gw.getActiveWindow()
        active_title = gwget.title if gwget else ''
        if all(i in active_title for i in data_program['active window name']):
            last_dt_window_active = dt

        # update mouse_move
        old_mouse_pos = mouse_pos
        mouse_pos = pyautogui.position()
        if mouse_pos != old_mouse_pos:
            last_dt_mouse_move = dt

        if (dt - old_dt).total_seconds() > 1:
            old_dt = dt
            # 1sec
            ac_t_sec = (dt - last_dt_window_active).total_seconds()
            data_program['text1_output'] = f'{ac_t_sec:.0f}'
            if ac_t_sec < data_program["stop when window is not active"]:
                window_active_ok = True
            else:
                window_active_ok = False
            mo_t_sec = (dt - last_dt_mouse_move).total_seconds()
            data_program['text2_output'] = f'{mo_t_sec:.0f}'
            if mo_t_sec < data_program["stop when mouse is not moved"]:
                move_mouse_ok = True
            else:
                move_mouse_ok = False

            if window_active_ok and move_mouse_ok:
                ac_time += 1
                data_program['label'] = f'{ac_time} min'

            all_time += 1

            time_axis.append(int(datetime.now().timestamp()))
            window_active_axis.append(1 if window_active_ok else 0)
            mouse_moved_axis.append(1 if move_mouse_ok else 0)
            result_axis.append(1 if window_active_ok and move_mouse_ok else 0)

            if all_time % 5 == 0:
                save_data = True

        if save_data:
            save_data = False
            with open('data.json', 'w') as f:
                string = json.dumps({'time': time_axis,
                                     'window_active': window_active_axis,
                                     'mouse_moved': mouse_moved_axis,
                                     'result': result_axis}, indent=4)
                f.write(string)


def show(data_program):
    while data_program['play']:
        while data_program['show_ui'] and data_program['play']:
            pygame.init()
            width, height = 300, 400
            os.environ['SDL_VIDEO_WINDOW_POS'] = f'{1920 - width},{1080 - height - 48}'

            flags = pygame.NOFRAME
            display = pygame.display.set_mode((width, height), flags)
            display.fill((70, 0, 70))

            # Get the window handle
            hwnd = pygame.display.get_wm_info()["window"]
            print(hwnd)

            # # Set the extended window style to include WS_EX_TOOLWINDOW
            # GWL_EXSTYLE = -20
            # WS_EX_TOOLWINDOW = 0x80
            # style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            # ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TOOLWINDOW)

            # use Always On Top
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            # don't use Always On Top
            # win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            ui_manager = pygame_gui.UIManager((width, height), 'theme.json')
            close = pygame_gui.elements.UIButton(pygame.Rect(250, 5, 50, 30), 'X', ui_manager, )

            label1 = pygame_gui.elements.UILabel(pygame.Rect(30, 50, 200, 30), 'window is not active :', ui_manager)
            text1_output = pygame_gui.elements.UITextBox('', pygame.Rect(50, 50 + 30, 60, 30), ui_manager)
            text1_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(120, 50 + 30, 60, 30), ui_manager)
            text1_input.set_text(f'{data_program["stop when window is not active"]}')

            label1 = pygame_gui.elements.UILabel(pygame.Rect(30, 150, 200, 30), 'mouse is not moved :', ui_manager)
            text2_output = pygame_gui.elements.UITextBox('', pygame.Rect(50, 150 + 30, 60, 30), ui_manager)
            text2_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(120, 150 + 30, 60, 30), ui_manager)
            text2_input.set_text(f'{data_program["stop when mouse is not moved"]}')
            label = pygame_gui.elements.UILabel(pygame.Rect(30, 300, 120, 30), '- min', ui_manager)

            clock = pygame.time.Clock()

            old_dt = datetime.now()
            while data_program['play'] and data_program['show_ui']:
                dt = datetime.now()
                if (dt - old_dt).total_seconds() > 1:
                    old_dt = dt
                    # 1 sec
                    text1_output.set_text(data_program['text1_output'])
                    text2_output.set_text(data_program['text2_output'])
                    label.set_text(data_program['label'])

                time_delta = clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    ui_manager.process_events(event)
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == close:
                            data_program['show_ui'] = False
                            data_program['close ui'] = True
                    elif event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                            print(event)
                            if any(c not in '0123456789' for c in event.text):
                                _0_9 = re.sub(r'[^0-9]', '', event.text)
                                event.ui_element.set_text(_0_9)

                ui_manager.update(time_delta)
                display.fill((255, 255, 255))  # Fill the window with white
                ui_manager.draw_ui(display)
                pygame.display.flip()
            else:
                pygame.quit()

        else:
            time.sleep(1)


# try:
# except Exception as e:
#     if f'{e}' == 'screen grab failed':
#         continue
#     with open('log.txt', 'a') as f:
#         f.write(f'{datetime.now()} {e}\n')


if __name__ == '__main__':
    import multiprocessing

    manager = multiprocessing.Manager()
    data_program = manager.dict()

    # if not os.path.exists('data_program.json'):

    dic = {
        'show_ui': True,
    }
    with open('data_program.json', 'w') as f:
        f.write(json.dumps(dic, indent=4))

    data_program['close ui'] = False
    data_program['show_ui'] = dic['show_ui']
    data_program['play'] = True
    conf = configparser.ConfigParser()
    conf.read('config.ini')

    data_program['stop when window is not active'] = eval(conf['DEFAULT']['stop when window is not active'])
    data_program['stop when mouse is not moved'] = eval(conf['DEFAULT']['stop when mouse is not moved'])
    data_program['active window name'] = eval(conf['DEFAULT']['active window name'])
    # except:
    # conf = configparser.ConfigParser()
    # conf['DEFAULT']['stop when window is not active'] = '60'
    # conf['DEFAULT']['stops when mouse is not moved'] = '60'
    # conf['DEFAULT']['active window name'] = 'None'
    # with open('config.ini', 'w') as configfile:
    #     conf.write(configfile)
    #
    # stop_when_window_is_not_active = eval(conf['DEFAULT']['stop when window is not active'])
    # stop_when_mouse_is_not_moved = eval(conf['DEFAULT']['stop when mouse is not moved'])
    # active_window_name = eval(conf['DEFAULT']['active window name'])

    run_process = multiprocessing.Process(target=run, args=(data_program,))
    show_process = multiprocessing.Process(target=show, args=(data_program,))
    update_data_program_process = multiprocessing.Process(target=update_data_program, args=(data_program,))

    run_process.start()
    show_process.start()
    update_data_program_process.start()

    run_process.join()
    show_process.join()
    update_data_program_process.join()
