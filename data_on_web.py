import json
from datetime import datetime
from flask import Flask, request
import sys

def json_to_html(json_data):
    html = '<ul>\n'
    for key, value in json_data.items():
        html += f'<li><strong>{key}</strong>: '
        if isinstance(value, dict):
            html += json_to_html(value)
        else:
            html += f'''{value} {str(type(value)).replace("<class '", "(").replace("'>", ")")}'''
        html += '</li>\n'
    html += '</ul>\n'
    return html

def main(data):
    app = Flask(__name__)
    dataw = {'show ui': False, 'b': 6, 'c': {'k': 1, 'l': 2}}

    @app.route("/")
    def index():
        return json_to_html(dataw)

    @app.route("/api")
    def api():
        return json.dumps(dataw, indent=4)

    @app.route("/write")
    def write():
        if not data['run program']:
            print("Stopping the program.")
            sys.exit()

        for k, v in request.args.items():
            try:
                v = eval(v)
            except:
                pass
            dataw[k] = v

        return json_to_html(dataw)

    app.run()

if __name__ == '__main__':
    print('app ok')
    data = {'run program': True}
    main(data)
