import base64

from aiohttp import ClientSession

from core.config import config

URL = f"{config.OPENAI_BASE_URL}/voice/tts"


class TTS:
    def __init__(
        self, voice_type: str = "qiniu_zh_female_tmjxxy", speed_ratio: float = 1.0
    ):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        }
        self.voice_type = voice_type
        self.speed_ratio = speed_ratio

    async def post(
        self,
        text: str,
    ) -> dict:
        data = {
            "audio": {
                "voice_type": self.voice_type,
                "encoding": "mp3",
                "speed_ratio": self.speed_ratio,
            },
            "request": {"text": text},
        }

        async with ClientSession() as session:
            async with session.post(URL, headers=self.headers, json=data) as resp:
                return await resp.json()

    async def save_audio(self, text: str, filepath: str) -> None:
        result = await self.post(text)
        audio_base64 = result.get("data")
        if not audio_base64:
            raise ValueError(f"TTS 响应中未包含音频数据: {result}")

        audio_bytes = base64.b64decode(audio_base64)
        with open(filepath, "wb") as f:
            f.write(audio_bytes)
