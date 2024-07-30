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
def send_data(data):

    #배열 중복을 막기 위해서 다음과 같이 설정
    filtered_data, extracted_numbers = data
    unique_numbers = list(set(filtered_data + extracted_numbers))

    url = 'http://localhost:8080/receive-data'

    print(url)
    response = requests.post(url, json={'data': unique_numbers})
    
    try:
        return response.json()
    except ValueError:
        return response.text
    


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
    return render_template('index.html',text=text)

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
        
        # 이미지 처리 로직 추가
        print(jsonify({"message": f'File successfully uploaded: {filename}'}))
    

     #업로드 된 처방전을 prescription.py로 호출.
        try:
            data = Final_Data.read_prescription(filename)
            
            #Spring으로 전달을 위해서 /send_data 호출.
            response_message = send_data(data)

            unique_numbers = list(set(data[0] + data[1]))
            session['text'] = unique_numbers

            
            
            return jsonify({"message": f'File successfully uploaded: {filename}', "response_message": response_message})
        
        except Exception as e:
            return jsonify({"message": f'파일 처리 중 오류 발생: {str(e)}'}), 500
    
    return jsonify({"message": '잘못된 파일입니다. 다시 시도하세요!'}), 400



#index.html 백엔드 테스트 전용 -> PostMan 대체 코드 
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
        
        #업로드 된 처방전을 prescription.py로 호출.
        try:
            data = Final_Data.read_prescription(filename)
            
            #Spring으로 전달을 위해서 /send_data 호출.
            response_message = send_data(data)

            unique_numbers = list(set(data[0] + data[1]))
            session['text'] = unique_numbers

            
            
            return redirect(url_for('index', message=f'파일이 성공적으로 업로드 되었습니다! -> {filename}. {response_message}'))
        
        except Exception as e:
            return redirect(url_for('index', message=f'파일 처리 중 오류 발생: {str(e)}'))
    
    return redirect(url_for('index', message='잘못된 파일입니다. 다시 시도하세요!'))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)