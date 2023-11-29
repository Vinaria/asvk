import json
import socket
from calculations import *

host = '0.0.0.0'
port = 8080
MSG_LEN = 16               # размер сообщения, содержащего длину передаваемой строки

got_data = 0
json_string = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    while 1:
        s.listen()
        conn, adr = s.accept()

        with conn:
            while 1:
                len_bytes = conn.recv(MSG_LEN)
                length = int.from_bytes(len_bytes, 'little')

                if length == 0:                                 # получили сообщение о конце связи
                    break

                try:                                            # ловим ошибки, вызванные неверным форматом
                    dec_data = conn.recv(length)                # входных данных
                    data = dec_data.decode()
                    result = find_main_node(data)

                except Exception:
                    result = "incorrect data"

                answer = json.dumps(result)
                answer_length = len(answer)
                conn.sendall(answer_length.to_bytes(MSG_LEN, 'little'))
                conn.sendall(answer.encode())
