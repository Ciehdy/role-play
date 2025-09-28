from fastapi import FastAPI, File, Request, UploadFile, WebSocket
from fastapi.templating import Jinja2Templates
from openai import AsyncOpenAI
from pydantic import BaseModel

from core.settings import settings
from domain.chat.asr import asr
from domain.chat.session import ChatSession
from domain.role.models import load_roles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = AsyncOpenAI(
    base_url=settings.openai.base_url,
    api_key=settings.openai.api_key,
)

roles = load_roles("roles.json")


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "ws_url": "/ws", "roles": roles},
    )


class ASRRequest(BaseModel):
    audio_base64: str


@app.post("/asr")
async def post_asr(file: UploadFile = File(...)):
    text = asr.transcribe(audio=file.file)
    return {"text": text}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, role: str):
    await websocket.accept()

    session = ChatSession(roles.get(role, next(iter(roles.values()))))

    try:
        while True:
            user_msg = await websocket.receive_text()
            await session.stream_message(user_msg, websocket)
    except Exception:
        await session.close()
