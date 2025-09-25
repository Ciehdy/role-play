from pathlib import Path

from pydantic import BaseModel, TypeAdapter


class Role(BaseModel):
    name: str
    description: str  # 人物的背景和性格描述
    prompt: str  # 额外提示词
    tts_voice_type: str
    tts_speed_ratio: float

    def system_prompt(self) -> str:
        base = f"You are {self.name}. {self.description}"
        if self.prompt:
            base += f" {self.prompt}"
        return base


def load_roles(file_path: str) -> dict[str, Role]:
    text = Path(file_path).read_text(encoding="utf-8")
    return TypeAdapter(dict[str, Role]).validate_json(text)
