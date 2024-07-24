# 백엔드 - 파이썬 파트

## 👨‍💻 Acting
![스크린샷 2024-07-24 오후 11 30 15](https://github.com/user-attachments/assets/1effaf0f-401d-459c-8573-90ab8ca4c1e1)

https://github.com/user-attachments/assets/fbb95002-b106-4a62-b26b-f45d6d5834b0


## Python환경에서 처방전 이미지 OCR 처리 (-> modules/prescription.py)
<pre><code>import easyocr
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
print(test.read_prescription())</code></pre>


## 💊 처방전 분류하기 

<h4>1. 보험번호(이하, 약 번호)가 있으면 숫자 추출 <br></h4>
<h4>2. 보험번호(이하, 약 번호)가 없다면 글자 추출 </h4>

<img width="1185" alt="스크린샷 2024-07-25 오전 12 31 30" src="https://github.com/user-attachments/assets/783fa9ee-3cf8-44d1-b7b5-3cbb8a4b73b9">

<h4>코드 정리중...</h4>
## ⚡️ spring <-> Flask 

<h3>[Flask에서 5133번 포트로 POST 요청]</h3>
<img width="884" alt="스크린샷 2024-07-24 오전 12 03 18" src="https://github.com/user-attachments/assets/4da34517-0b29-4358-8d33-fdd5167c9fbe">
<h3>[Spring에서 8080번 포트로 /receive-data 숫자 출력]</h3>
<img width="1337" alt="스크린샷 2024-07-24 오전 12 03 40" src="https://github.com/user-attachments/assets/23ddb11f-f3b9-402b-9ff3-731bcf3d43ad">



## ⚠️ commit 컨벤션

```
{태그}: {클래스 이름} {커밋 메시지}
```

- 💡 예시: `[Feat] 회원 가입 기능 구현`
- 커밋 내용은 명사로 끝나며 마침표를 사용하지 않는다.

### 태그

- 이모지는 선택에 따라 활용한다.

| 태그       | 설명                      |
|:---------|:------------------------|
| Feat     | 새로운 기능 구현               |
| Fix      | 버그, 오류 수정                   |
| Docs     | README와 같은 문서 수정        |
| Test     | 테스트 코드 추가 및 업데이트        |
| Refactor | 코드 리팩토링                 |
| Comment  | 주석 추가(코드 변경 X) 혹은 오타 수정 |
| Merge    | 다른 브랜치를 merge 할 때 사용                   |
| Add   | Feat 이외의 부수적인 코드 추가, 라이브러리 추가, 새로운 파일 생성 시        |
| Rename   | 파일 이름 변경        |
| Move   | 프로젝트 내 파일이나 코드의 이동        |
