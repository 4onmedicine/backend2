import easyocr
import json
import re
from env import DEBUG

# GPU/CPU 모드 선택 가능
reader = easyocr.Reader(['ko', 'en'], gpu=DEBUG.GPU)

json_result = []

class Prescription:

    def __init__(self):
        # 정규식 패턴: 8~9자리 숫자
        self.pattern = re.compile(r'\b\d{8,9}\b')

    def read_prescription(self, filename):
        self.filename = filename
        print("파일경로")
        print(self.filename)
        result = reader.readtext(self.filename)

        # 약 품목 코드가 없는 경우 
        include_keywords = ['정', '캡슐', '약', '정제']
        exclude_keywords = ['복약안내', '약제비', '환자정보', '조제약사', '노란색 정제', '하얀색 정제', '약국', '의원', '병원', '흰색 정제', '노랑색 정제', '약품명', '주의사항', '약품사진', '항갈색 정제']

        filtered_data = []

        # 약물 정보를 필터링하여 저장할 리스트
        for bbox, text, confidence in result:
            # 제외할 키워드가 포함되어 있지 않고, 포함할 키워드가 포함되어 있는 경우에만 추가
            if not any(exclude_keyword in text for exclude_keyword in exclude_keywords) and \
            any(include_keyword in text for include_keyword in include_keywords):
                filtered_data.append(text)

        print(filtered_data)

        # 약 품목 코드가 있는 경우 
        for detection in result:
            _, text, confidence = detection
            match = self.pattern.search(text)
            if match:
                json_result.append({
                    'data': match.group()
                })

        # 원하는 형식으로 출력
        json_output = json.dumps({
            "response_message": json_result
        }, ensure_ascii=False, indent=4)

        print(json_output)

        return json_output
