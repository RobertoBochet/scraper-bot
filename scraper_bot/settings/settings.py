from datetime import timedelta
from pathlib import Path
from typing import Annotated, ClassVar, Self, Type

from pydantic import BaseModel, Field, HttpUrl, RedisDsn
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

DEFAULT_SETTINGS_PATH = [
    Path.cwd() / "config.yml",
    Path.cwd() / "config.yaml",
    "/etc/scraper_bot/config.yml",
    "/etc/scraper_bot/config.yaml",
]


class Task(BaseModel):
    name: Annotated[str, Field(description="A human readable label for teh task")]
    url: Annotated[
        HttpUrl, Field(description="The url to the page to be scraped. Use `{i}` as a placeholder for the pagination")
    ]
    target: Annotated[
        str,
        Field(description="It is a unique css selector to target the <a> tag contains the link to the scraped page"),
    ]
    interval: Annotated[timedelta, Field(gt=0, description="How often the task should be done expressed in seconds")]


class BotSettings(BaseSettings):
    token: Annotated[
        str, Field(pattern=r"^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$", description="The bot token provided by @BotFather")
    ]
    chats: Annotated[
        list[int],
        Field(description="It is a list of user_id or group_id where the scraped entities will have to be sent"),
    ]


class Settings(BaseSettings):
    tasks: Annotated[list[Task], Field(min_length=1)]
    bot: Annotated[BotSettings, Field(description="Telegram bot configuration")]
    redis: Annotated[RedisDsn, Field(description="An URI to a redis instance used to cache")]

    model_config = SettingsConfigDict(extra="ignore")

    _SETTINGS_PATH: ClassVar[str | Path | list[str | Path]] = DEFAULT_SETTINGS_PATH

    @classmethod
    def set_settings_path(cls, settings_path: str | Path | list[str | Path]) -> None:
        cls._SETTINGS_PATH = settings_path

    @classmethod
    def settings_customise_sources(
        cls, settings_cls: Type[BaseSettings], **kwargs
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            EnvSettingsSource(
                settings_cls,
                env_prefix="SB__",
                env_nested_delimiter="__",
                case_sensitive=False,
            ),
            YamlConfigSettingsSource(settings_cls, yaml_file=cls._SETTINGS_PATH),
        )

    _instance: ClassVar[Self | None] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
