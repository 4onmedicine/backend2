from flask import Flask, request, redirect, render_template, url_for, jsonify
from env import FLASK_ENUM
from modules.prescription import Prescription
import requests

app = Flask(__name__, static_url_path='/static')

Final_Data = Prescription()

@app.route('/send_data', methods=['POST'])
def send_data():
    data = Final_Data.read_prescription()

    #배열 중복을 막기 위해서 다음과 같이 설정
    unique_numbers = list(set(data))

    url = 'http://localhost:8080/receive-data'

    print(url)
    response = requests.post(url, json=unique_numbers)
    
    if response.headers['Content-Type'] == 'application/json':
        return jsonify(response.json())
    else:
        return response.text
    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)