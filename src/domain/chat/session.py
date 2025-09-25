from typing import Literal

from fastapi import WebSocket
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

from core.config import config
from domain.chat.tts import TTS
from domain.role.models import Role


class Message(BaseModel):
    type: Literal["text", "audio", "eot"]
    data: str | None


class ChatSession:
    def __init__(self, role: Role):
        self.client = AsyncOpenAI(
            base_url=config.OPENAI_BASE_URL,
            api_key=config.OPENAI_API_KEY,
        )
        self.role = role
        self.tts = TTS(voice_type=role.tts_voice_type, speed_ratio=role.tts_speed_ratio)
        # 保存会话历史
        self.history: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.role.system_prompt()}
        ]

    async def send_ws(self, websocket: WebSocket, message: Message):
        await websocket.send_text(message.model_dump_json())

    async def stream_message(self, message: str, websocket: WebSocket):
        self.history.append({"role": "user", "content": message})

        response = await self.client.chat.completions.create(
            model="deepseek-v3",
            messages=self.history,
            stream=True,
            max_tokens=4096,
        )

        reply_buffer = ""

        async for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                reply_buffer += delta
                # 逐片段推送给前端
                await self.send_ws(websocket, Message(type="text", data=delta))

        # 调用 TTS 接口生成音频
        audio_b64 = (await self.tts.post(text=reply_buffer)).data
        await self.send_ws(websocket, Message(type="audio", data=audio_b64))

        # 流结束时发 EOT
        await self.send_ws(websocket, Message(type="eot", data=None))

        # 最终完整回复加入历史
        self.history.append({"role": "assistant", "content": reply_buffer})

    async def close(self):
        await self.client.close()
