import os

from dotenv import load_dotenv


class Config:
    OPENAI_BASE_URL: str
    OPENAI_API_KEY: str

    def __init__(self):
        load_dotenv()
        self.OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


config = Config()
