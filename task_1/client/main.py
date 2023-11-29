import socket
import json
import os
from flask import Flask, jsonify
app = Flask(__name__)

host_name = 'server'
port = 8080

directory = 'data'
MSG_LEN = 16               # размер сообщения, содержащего длину передаваемой строки


@app.route('/', methods=['GET'])
def make_request():
    report = {}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host_name, port))

        for f in os.scandir(directory):
            if f.is_file() and f.path.split('.')[-1].lower() == 'json':
                with open(f.path, 'r') as json_file:
                    json_string = json_file.read()
            else:
                continue

            length = len(json_string)
            if length == 0:
                report[f.path] = "empty file"
                continue

            s.sendall(length.to_bytes(MSG_LEN, 'little'))   # отправляем длину сообщения в байтах
                                                            # и потом само сообщение

            answer_len_b = s.recv(MSG_LEN)
            answer_length = int.from_bytes(answer_len_b, 'little')
            json_answer = s.recv(MSG_LEN).decode()
            answer = json.loads(json_answer)

            report[f.path] = answer

        length = 0                         # отправляем сообщение о конце связи
        s.sendall(length.to_bytes(MSG_LEN, 'little'))
    return jsonify(report)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5051', debug=True)













