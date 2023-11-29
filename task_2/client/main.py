import json
import requests
import os
from flask import Flask, jsonify
app = Flask(__name__)

url = 'http://server:8080'
directory = 'data'


@app.route('/', methods=['GET'])
def make_request():
    for f in os.scandir(directory):
        if f.is_file() and f.path.split('.')[-1].lower() == 'json':
            with open(f.path, 'r') as json_file:
                json_string = json_file.read()
        else:
            continue
        response = requests.post(url, json=json_string)
        answer = response.json()
        report[f.path] = answer
    return jsonify(report)


if __name__ == '__main__':
    report = {}


    app.run(host='0.0.0.0', port='8081', debug=True)
