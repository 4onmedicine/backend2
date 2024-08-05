# Backend - Python Part(Server)

## 🖥️ Schema
![KakaoTalk_Photo_2024-08-05-20-21-46](https://github.com/user-attachments/assets/859a41ee-f18d-4e4f-a16a-c8693c55550e)

## 👨‍💻 Acting
<h3>처방전 이미지에서 '보험코드' 만을 추출하여 검색</h3>
<h4>PostMan에서 form-data 파일형식으로 Flask에서 OCR변환후 Spring 서버에 전송</h4>
<img width="915" alt="스크린샷 2024-08-01 오전 8 48 08" src="https://github.com/user-attachments/assets/caa90151-17c5-444b-b966-5e20235b169d">

<h3>추출된 '보험코드'를 통해서 약품 정보 검색</h3>
<h4>PostMan에서 Json타입으로 data 전송</h4>
<img width="879" alt="스크린샷 2024-08-01 오전 8 50 58" src="https://github.com/user-attachments/assets/494872e5-c72c-4aa0-9ea1-8c6e5d8cf3e9">

## 👨‍⚕️ Prescription Example
<h4>처방전 예시</h4>

![처방전_최종001001 (1)](https://github.com/user-attachments/assets/15813496-6642-46d8-a1ec-8dadf432bb24)


## 💊 처방전 분류하기 

<h4>1. 보험번호(이하, 약 번호)가 있으면 숫자 추출 <br></h4>
<h4>2. 보험번호(이하, 약 번호)가 없다면 글자 추출 </h4>

<img width="1185" alt="스크린샷 2024-07-25 오전 12 31 30" src="https://github.com/user-attachments/assets/783fa9ee-3cf8-44d1-b7b5-3cbb8a4b73b9">

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
