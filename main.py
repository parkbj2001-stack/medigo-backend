from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# CORS 설정 – 웹앱 연동을 위한 필수 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API 키 설정 – 환경변수 또는 직접 입력
openai.api_key = "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"

# 요청받을 데이터 형식 정의
class Request(BaseModel):
    text: str

# POST 요청 처리 (예: /diagnose)
@app.post("/diagnose")
async def diagnose(req: Request):
    user_input = req.text

    # GPT에 보낼 프롬프트 (사용자 입력 포함)
    prompt = (
        f"A user described the following symptom:\n\"{user_input}\"\n\n"
        "As an AI-powered medical assistant, provide a comprehensive and detailed response in English. "
        "Include possible causes, conditions to consider, when to seek medical help, and general recommendations. "
        "Use clear and accessible medical language, and present your answer in a way that is easy to understand for a non-medical person."
    )

    # GPT 호출
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a compassionate and thorough medical assistant. "
                           "Respond in English with clear and detailed explanations suitable for everyday users."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=800,
    )

    reply = response.choices[0].message.content

    # 프론트엔드로 보낼 응답 형식
    return {
        "messages": [
            {"sender": "bot", "message_text": reply}
        ]
    }
