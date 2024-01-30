import time

if __name__ == '__main__':
    from datetime import datetime
    import multiprocessing
    import requests
    from flask import Flask, request
    import json
    from pprint import pprint

    import program_icon
    from pygame_ui import ui
    import data_on_web

    manager = multiprocessing.Manager()
    data = manager.dict()
    data['run program'] = True
    data_process = multiprocessing.Process(target=data_on_web.main, args=(data,))
    ui_process = multiprocessing.Process(target=ui, args=(data,))
    main_process = multiprocessing.Process(target=program_icon.main, args=(data,))

    data_process.start()
    # ui_process.start()
    # main_process.start()

    data_process.join()
    # ui_process.join()
    # main_process.join()
