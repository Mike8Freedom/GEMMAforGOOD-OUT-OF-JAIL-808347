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
    body = await request.json()
    response = client.chat.completions.create(
        model="nvidia/Gemma-4-31B-IT-NVFP4:featherless-ai",
        messages=body.get("messages", []),
        temperature=0.7,
        max_tokens=400
    )
    return response.model_dump()

@app.get("/health")
async def health():
    return {"status": "Gemma 4 proxy online"}
