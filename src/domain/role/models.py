from dataclasses import dataclass


@dataclass
class Role:
    name: str
    description: str
    tts_voice_type: str
    tts_speed_ratio: float

    def to_system_prompt(self) -> str:
        return (
            f"You are {self.name}. {self.description} "
            f"Always reply in the tone and style of {self.description}."
        )
