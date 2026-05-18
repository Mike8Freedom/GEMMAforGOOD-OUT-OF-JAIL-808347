from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

@app.post("/v1/chat/completions")
async def chat(request: Request):
    try:
        body = await request.json()
        
        response = client.chat.completions.create(
            model="nvidia/Gemma-4-31B-IT-NVFP4:featherless-ai",
            messages=body.get("messages", []),
            temperature=0.65,      # чуть ниже
            max_tokens=180,        # сильно уменьшил — это важно!
            stream=False
        )
        
        return response.model_dump()
    
    except Exception as e:
        return {"choices": [{"message": {"role": "assistant", "content": "I'm having trouble thinking right now..."}}]}

@app.get("/health")
async def health():
    return {"status": "Gemma 4 proxy online"}
