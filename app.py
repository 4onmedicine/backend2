from flask import Flask, request, redirect, render_template, url_for, jsonify, session
from env import FLASK_ENUM, OPENAI
from modules.prescription import Prescription
import requests
from pydantic import BaseModel, ValidationError
import openai
import json
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = FLASK_ENUM.KEY

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

openai.api_key = OPENAI.KEY

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

Final_Data = Prescription()

@app.route('/send_data', methods=['POST'])
def send_data():
    try:
        # JSON 데이터 가져오기
        data = request.json
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400
        
        filtered_data = data.get('response_message', [])
        if not isinstance(filtered_data, list):
            return jsonify({"error": "Invalid data format. Expected 'response_message' to be a list."}), 400
        
        # 문자열로 된 JSON 객체를 파싱하여 JSON 객체 리스트로 변환
        parsed_data = []
        for item in filtered_data:
            try:
                parsed_data.append(json.loads(item))  # 문자열을 JSON 객체로 변환
            except json.JSONDecodeError:
                return jsonify({"error": "Failed to parse JSON data"}), 400
            
        print("Received data:", filtered_data)

        url = 'https://4onmserver.kro.kr/receive-data'
        headers = {'Content-Type': 'application/json'}
        
        # JSON 객체를 문자열로 변환하며 중복 제거
        unique_data_set = {json.dumps(d, sort_keys=True) for d in parsed_data}
        unique_data = [json.loads(d) for d in unique_data_set]
        print("Filtered data:", unique_data)

        # 'data' 키를 사용하여 JSON 데이터 전송
        response = requests.post(url, json={'data': unique_data}, headers=headers)
        
        print(response)

        # 응답 내용 확인
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)
        
        try:
            response_json = response.json()
        except ValueError as e:
            return jsonify({"error": f"Invalid JSON response from server: {str(e)}"}), 500
        
        return jsonify(response_json)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    if request.content_type != 'application/json':
        return jsonify({"detail": "Content-Type must be application/json"}), 400

    try:
        data = request.get_json()
        if isinstance(data.get('message'), list):
            data['message'] = ' '.join(data['message'])  # 리스트를 문자열로 변환
        print(data)
        chat_request = ChatRequest(**data)
    except (TypeError, ValidationError) as e:
        return jsonify({"detail": str(e)}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 모델 선택
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chat_request.message}
            ]
        )
        chat_response = ChatResponse(response=response.choices[0].message['content'].strip())
        return jsonify(chat_response.dict())
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route('/')
def index():
    text = session.get('text', '')
    return render_template('index.html', text=text)

@app.route('/upload_flask', methods=['POST'])
def upload_flask():
    if 'file' not in request.files:
        return jsonify({"message": 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": 'No selected file'}), 400

    if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        try:
            print(filename)
            json_output = Final_Data.read_prescription(filename)
        
                
            try:
                data = json.loads(json_output)
            except json.JSONDecodeError as e:
                return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400
            
            if not isinstance(data, dict):
                return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400
            

            response_message = data.get('response_message', [])
            

            unique_data = list({json.dumps(item, sort_keys=True) for item in response_message})
            
 
            try:
                unique_data = [json.loads(item) for item in unique_data]
            except json.JSONDecodeError as e:
                return jsonify({"error": f"Failed to parse unique data: {str(e)}"}), 400
            
          
            insurance_codes = [item['data'] for item in unique_data if 'data' in item]
            
    
            return jsonify({"data": insurance_codes})
        
        except Exception as e:
            # 처리 중 예외 발생 시 오류 메시지 반환
            return jsonify({"error": str(e)}), 500

# index.html 백엔드 테스트 전용 -> PostMan 대체 코드 
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index', message='No file part'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index', message='선택된 파일이 없습니다.'))
    
    if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        try:
            print(filename)
            data = Final_Data.read_prescription(filename)
            
            # Spring 서버로 전달
            response_message = requests.post('http://localhost:8080/send-data', json=data).json()

            unique_numbers = list(set(data[0] + data[1]))
            session['text'] = unique_numbers

            return redirect(url_for('index', message=f'파일이 성공적으로 업로드 되었습니다! -> {filename}. {response_message}'))
        
        except Exception as e:
            return redirect(url_for('index', message=f'파일 처리 중 오류 발생: {str(e)}'))
    
    return redirect(url_for('index', message='잘못된 파일입니다. 다시 시도하세요!'))

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)
