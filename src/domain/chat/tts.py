from aiohttp import ClientSession
from pydantic import BaseModel

from core.settings import settings

_URL = f"{settings.openai.base_url}/voice/tts"


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
        self.voice_type = voice_type
        self.speed_ratio = speed_ratio

    async def post(self, text: str):
        payload = TTSRequest(
            audio=Audio(voice_type=self.voice_type, speed_ratio=self.speed_ratio),
            request=Request(text=text),
        )

        async with ClientSession() as session:
            async with session.post(
                _URL, headers=settings.qiniu_headers, json=payload.model_dump()
            ) as resp:
                j = await resp.json()
                return TTSResponse.model_validate(j)
