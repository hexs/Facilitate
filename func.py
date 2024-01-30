import json
import requests


def req(path):
    url = 'http://127.0.0.1:5000'
    try:
        r = requests.get(f'{url}/{path}')
        text = r.text
    except requests.exceptions.Timeout:
        print('Timeout')
        text = ''
    except requests.exceptions.RequestException as e:
        print(e)
        text = ''
    return text


def req_dict(path):
    url = 'http://127.0.0.1:5000'
    try:
        r = requests.get(f'{url}/{path}')
        dic_data = json.loads(r.text)
    except requests.exceptions.Timeout:
        print('Timeout')
        dic_data = {}
    except requests.exceptions.RequestException as e:
        print(e)
        dic_data = {}
    return dic_data
