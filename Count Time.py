import configparser
import json
import os
from datetime import datetime
import pyautogui
import ctypes
import win32gui
import win32con
import pygame
import pygetwindow as gw
import graph

def write_to_config_file():
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)


conf = configparser.ConfigParser()
conf.read('config.ini')
try:
    eval(conf['DEFAULT']['stop when window is not active'])
    eval(conf['DEFAULT']['stop when mouse is not moved'])
except:
    conf['DEFAULT']['stop when window is not active'] = '60'
    conf['DEFAULT']['stop when mouse is not moved'] = '60'
    eval(conf['DEFAULT']['stop when window is not active'])
    eval(conf['DEFAULT']['stop when mouse is not moved'])
try:
    eval(conf['DEFAULT']['active window name'])
except:
    conf['DEFAULT']['active window name'] = "['name','program']"
    eval(conf['DEFAULT']['active window name'])
conf['DEFAULT']['stop program'] = '0'

try:
    width = eval(conf['DEFAULT']['width'])
    height = eval(conf['DEFAULT']['height'])
except:
    conf['DEFAULT']['width'] = '280'
    conf['DEFAULT']['height'] = '48'
    width = eval(conf['DEFAULT']['width'])
    height = eval(conf['DEFAULT']['height'])

try:
    x = eval(conf['DEFAULT']['WINDOW_POS_X'])
    y = eval(conf['DEFAULT']['WINDOW_POS_Y'])
except:
    conf['DEFAULT']['WINDOW_POS_X'] = '1520'
    conf['DEFAULT']['WINDOW_POS_Y'] = '1080'
    x = eval(conf['DEFAULT']['WINDOW_POS_X'])
    y = eval(conf['DEFAULT']['WINDOW_POS_Y'])

WHITE = (255, 255, 255)
GREEN = (0, 150, 10)
RED = (128, 0, 10)
BLACK = 0, 0, 0

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x - width},{y - height}'
display = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption('Count Time')

# Get the window handle
hwnd = pygame.display.get_wm_info()["window"]
conf['DEFAULT']['hwnd'] = f'{hwnd}'
write_to_config_file()

# Set the extended window style to include WS_EX_TOOLWINDOW
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x80
style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TOOLWINDOW)
# use Always On Top
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
font = pygame.font.Font('Roboto-Medium.ttf', 16)
all_time_font = pygame.font.Font('Roboto-Medium.ttf', 18)

# --- run ---
try:
    with open('data.json') as f:
        data = json.loads(f.read())
    time_axis = data['time']
    window_active_axis = data['window_active']
    mouse_moved_axis = data['mouse_moved']
    result_axis = data['result']
except:
    time_axis = []
    window_active_axis = []
    mouse_moved_axis = []
    result_axis = []

window_active_ok = True
move_mouse_ok = True
ac_t_sec = 0
mo_t_sec = 0
all_time = len(result_axis)  # เวลาทั้งหมดที่เปิดโปรแกรม
ac_time = result_axis.count(1)  # เวลาที่ทำงาน
dict_img = graph.run()
dt = datetime.now()
ymd = f'{dt.year}-{dt.month}-{dt.day}'
if ymd in dict_img:
    ac_today_time = dict_img[ymd]['second']
else:
    ac_today_time = 0
print(ac_today_time)

last_dt_window_active = datetime.now()
last_dt_mouse_move = datetime.now()
mouse_pos = pyautogui.position()
old_dt = datetime.now()
save_data = False

while conf['DEFAULT']['stop program'] == '0':
    # read config file
    conf.read('config.ini')

    # show on top
    pygame_window = gw.getWindowsWithTitle("Count Time")
    if pygame_window:
        pygame_window[0].move(0, 0)

    # --- run ---
    dt = datetime.now()
    # update window_active
    gwget = gw.getActiveWindow()
    active_title = gwget.title if gwget else ''
    if all(i in active_title for i in eval(conf['DEFAULT']['active window name'])):
        last_dt_window_active = dt
    # update mouse_move
    old_mouse_pos = mouse_pos
    mouse_pos = pyautogui.position()
    if mouse_pos != old_mouse_pos:
        last_dt_mouse_move = dt

    # 1sec
    if (dt - old_dt).total_seconds() > 1:
        old_dt = dt
        ac_t_sec = (dt - last_dt_window_active).total_seconds()
        if ac_t_sec < eval(conf['DEFAULT']['stop when window is not active']):
            window_active_ok = True
        else:
            window_active_ok = False
        mo_t_sec = (dt - last_dt_mouse_move).total_seconds()

        if mo_t_sec < eval(conf['DEFAULT']['stop when mouse is not moved']):
            move_mouse_ok = True
        else:
            move_mouse_ok = False

        if window_active_ok and move_mouse_ok:
            ac_time += 1
            ac_today_time += 1
        all_time += 1

        time_axis.append(int(datetime.now().timestamp()))
        window_active_axis.append(1 if window_active_ok else 0)
        mouse_moved_axis.append(1 if move_mouse_ok else 0)
        result_axis.append(1 if window_active_ok and move_mouse_ok else 0)

        if all_time % 5 == 0:
            save_data = True

        all_windows = [win.title for win in gw.getAllWindows()]
        with open('all_windows.json', 'w') as f:
            f.write(json.dumps(all_windows, indent=4))

    if save_data:
        save_data = False
        with open('data.json', 'w') as f:
            string = json.dumps({'time': time_axis,
                                 'window_active': window_active_axis,
                                 'mouse_moved': mouse_moved_axis,
                                 'result': result_axis}, indent=4)
            f.write(string)

    # ui
    display.fill(WHITE)
    pygame.draw.rect(display, (150,) * 3, pygame.Rect(0, 0, width, height), 1)
    text1 = font.render(f'Window active: {ac_t_sec:.0f}', True, GREEN if window_active_ok else RED)
    textRect1 = text1.get_rect()
    textRect1.topleft = (4, 2)
    text2 = font.render(f'Mouse moved: {mo_t_sec:.0f}', True, GREEN if move_mouse_ok else RED)
    textRect2 = text2.get_rect()
    textRect2.topleft = (4, 23)
    text3 = all_time_font.render(f'{ac_today_time / 60:.1f} min', True, BLACK)
    textRect3 = text3.get_rect()
    textRect3.right = width - 4
    textRect3.centery = height / 2
    display.blit(text1, textRect1)
    display.blit(text2, textRect2)
    display.blit(text3, textRect3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()
