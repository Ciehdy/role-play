from openai import AsyncOpenAI

from core.config import config
from domain.role.models import Role
from tts import TTS


class ChatSession:
    def __init__(self, role: Role):
        self.client = AsyncOpenAI(
            base_url=config.OPENAI_BASE_URL,
            api_key=config.OPENAI_API_KEY,
        )
        self.role = role
        self.tts = TTS(voice_type=role.tts_voice_type, speed_ratio=role.tts_speed_ratio)

    async def send_message(self, message):
        response = await self.client.chat.completions.create(
            model="deepseek-v3",
            messages=[
                {"role": "system", "content": self.role.to_system_prompt()},
                {"role": "user", "content": message},
            ],
            stream=True,
            max_tokens=4096,
        )
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()  # 换行

    async def close(self):
        await self.tts.client.close()
        await self.client.close()
