from typing import BinaryIO

import numpy as np
from faster_whisper import WhisperModel

from core.settings import settings


class ASR:
    def __init__(self):
        self.model = WhisperModel(
            settings.asr.model,
            device=settings.asr.device,
            compute_type=settings.asr.compute_type,
        )

    def transcribe(self, audio: str | BinaryIO | np.ndarray) -> str:
        segments, _ = self.model.transcribe(
            audio,
            language=settings.asr.language,
            initial_prompt="以下是普通话的句子。",
        )
        return " ".join([segment.text for segment in segments])


asr = ASR()
