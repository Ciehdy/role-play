from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from openai import AsyncOpenAI

from core.config import config
from domain.chat.session import ChatSession
from domain.role.models import load_roles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = AsyncOpenAI(
    base_url=config.OPENAI_BASE_URL,
    api_key=config.OPENAI_API_KEY,
)

roles = load_roles("roles.json")


@app.get("/")
async def get(request: Request):
    ws_url = "ws://localhost:8000/ws"
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "ws_url": ws_url, "roles": roles},
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, role: str):
    await websocket.accept()

    session = ChatSession(roles.get(role, roles["xiao_yan"]))

    try:
        while True:
            user_msg = await websocket.receive_text()
            await session.stream_message(user_msg, websocket)
    except Exception:
        await session.close()
