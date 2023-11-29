import json
import requests
from calculations import *
from flask import Flask, request
app = Flask(__name__)

report = ''


json_string = """[[["A", "B"], ["B", "C"], ["C", "D"]], {"A": 10, "B": 20, "C": 10, "D" : 20}]"""


@app.route('/', methods=['POST'])
def handle_request():
    global report
    request_data = request.get_json()
    report += request_data
    try:
        a, b = json.loads(request_data)
        answer = json.dumps(find_main_node(a, b))
    except Exception:
        answer = json.dumps("incorrect data format")
    report += '\n' + answer
    print(report)
    return answer


@app.route('/', methods=['GET'])
def no_request():
    return report


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)






"""
class Observatory(Resource):
    def get(self):
        return {
            'Galaxies': ['Milkyway', 'Andromeda',
            'Large Magellanic Cloud (LMC)']
        }

api.add_resource(Observatory, '/')


# with open("/input_data.json", 'r') as file:
#    data = json.load(file)


"""




