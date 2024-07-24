from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

# OpenAI API 키 설정
openai.api_key = "sk-proj-iGbZb12pf9IPHGTDLmehT3BlbkFJdWRJ2FMvKPZW4ZjapWPB"


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 모델 선택
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.message}
            ]
        )
        return ChatResponse(response=response.choices[0].message['content'].strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 서버 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
