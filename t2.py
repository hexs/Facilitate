import time
from pprint import pprint

import pygetwindow as gw

def get_active_window_title():
    active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)
    return active_window[0].title if active_window else None

while True:
    all_windows = [win.title for win in gw.getAllWindows()]
    active_window = gw.getActiveWindow().title if gw.getActiveWindow() else None
    pprint(all_windows)
    print(active_window)
    print(type(active_window))
    time.sleep(0.5)
#
# if __name__ == "__main__":
#     active_window_title = get_active_window_title()
#     print(f"{active_window_title}")