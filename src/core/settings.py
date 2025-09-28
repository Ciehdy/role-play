from typing import Literal

from openai import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class OpenAISettings(BaseModel):
    base_url: str = ""
    api_key: str = ""


class QiniuSettings(BaseModel):
    access_key: str = ""
    secret_key: str = ""
    bucket_name: str = ""


class ASRSettings(BaseModel):
    model: str = "turbo"
    language: str | None = None
    device: Literal["cpu", "cuda"] = "cpu"
    compute_type: Literal["float16", "float32", "int8"] = "float32"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        toml_file="config.toml",
        env_nested_delimiter="__",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )

    openai: OpenAISettings = OpenAISettings()
    qiniu: QiniuSettings = QiniuSettings()
    asr: ASRSettings = ASRSettings()

    @property
    def qiniu_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai.api_key}",
        }


settings = AppSettings()
