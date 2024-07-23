import easyocr
import json
import re
from env import DEBUG


#GPU/CPU 모드 선택 가능
reader = easyocr.Reader(['ko', 'en'], gpu=DEBUG.GPU)
result = reader.readtext("src/img/prescription_1.jpeg")

json_result = []

# 정규식 패턴: 8~9자리 숫자
pattern = re.compile(r'\b\d{8,9}\b')

class Prescription:

    def __init__(self):
        pass

    def read_prescription(self):
        # 약 품목 코드가 있는 경우 
        for detection in result:
            _, text, confidence = detection
            if pattern.search(text):
                json_result.append({
                    'text': text,
                    'confidence': confidence
                })

        json_output = json.dumps(json_result, ensure_ascii=False, indent=4)
        print(json_output)

        extracted_numbers = []

        for item in json_result:
            text = item['text']
            match = pattern.search(text)
            if match:
                extracted_numbers.append(match.group())

        print(extracted_numbers)

        return extracted_numbers

test = Prescription()
print(test.read_prescription())
