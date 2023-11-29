import os
import json
from calculations import *

directory = 'data'
report = {}

for f in os.scandir(directory):
    if f.is_file() and f.path.split('.')[-1].lower() == 'json':
        with open(f.path, 'r') as json_file:
            json_string = json_file.read()
    else:
        continue

    if len(json_string) == 0:
        report[f.path] = "empty file"
        continue

    try:                                    # ловим ошибки, связанные с неверным форматом данных в файле
        a, b = json.loads(json_string)
        answer = find_main_node(a, b)
    except Exception:
        answer = "incorrect data format"

    report[f.path] = answer

print(json.dumps(report, indent=4))




