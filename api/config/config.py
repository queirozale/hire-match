from typing import Tuple, Type

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class Config(BaseSettings):
    database: SecretStr = Field(
        default=SecretStr(""),
        description="Mongo Database",
    )
    users_collection: SecretStr = Field(
        default=SecretStr(""),
        description="Users Collection",
    )
    resumes_collection: SecretStr = Field(
        default=SecretStr(""),
        description="Resumes Collection",
    )
        
    # local_path: str = Field(frozen=True, description="Local FAISS path")

    model_config = SettingsConfigDict(
        env_file=".env",
        yaml_file="api/config/config.yaml",
        yaml_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(settings_cls),
            dotenv_settings,
            env_settings,
            init_settings,
            file_secret_settings,
        )