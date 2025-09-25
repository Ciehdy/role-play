import base64

from aiohttp import ClientSession
from pydantic import BaseModel

from core.config import config

URL = f"{config.OPENAI_BASE_URL}/voice/tts"


class Audio(BaseModel):
    voice_type: str
    encoding: str = "mp3"
    speed_ratio: float = 1.0


class Request(BaseModel):
    text: str


class TTSRequest(BaseModel):
    audio: Audio
    request: Request


class Addition(BaseModel):
    duration: str


class TTSResponse(BaseModel):
    reqid: str
    operation: str
    sequence: int
    data: str
    addition: Addition


class TTS:
    def __init__(self, voice_type: str, speed_ratio: float = 1.0):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        }
        self.voice_type = voice_type
        self.speed_ratio = speed_ratio

    async def post(self, text: str):
        payload = TTSRequest(
            audio=Audio(voice_type=self.voice_type, speed_ratio=self.speed_ratio),
            request=Request(text=text),
        )

        async with ClientSession() as session:
            async with session.post(
                URL, headers=self.headers, json=payload.dict()
            ) as resp:
                j = await resp.json()
                return TTSResponse.model_validate(j)

    async def save_audio(self, text: str, filepath: str) -> None:
        result = await self.post(text)
        audio_base64: str = result.data
        if not audio_base64:
            raise ValueError(f"TTS 响应中未包含音频数据: {result}")

        audio_bytes = base64.b64decode(audio_base64)
        with open(filepath, "wb") as f:
            f.write(audio_bytes)
