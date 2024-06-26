from datetime import timedelta
from pathlib import Path
from typing import Annotated, ClassVar, Self, Type

from pydantic import Field, RedisDsn
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from .browser import BrowserSettings
from .notifications import NotificationsSettings
from .task import TaskSettings

DEFAULT_SETTINGS_PATH = [
    Path.cwd() / "config.yml",
    Path.cwd() / "config.yaml",
    "/etc/scraper_bot/config.yml",
    "/etc/scraper_bot/config.yaml",
]


class Settings(BaseSettings):
    daemonize: Annotated[
        bool, Field(description="make the scraper run as a daemon instead run only once", default=False)
    ]
    interval: Annotated[
        timedelta,
        Field(
            gt=0,
            description="How often the tasks should be done expressed in seconds. "
            "It will be ignored if `daemonize` is False",
            default=60 * 60,
        ),
    ]

    browser: Annotated[BrowserSettings, Field(description="Browser to use with playwright", default=BrowserSettings())]

    tasks: Annotated[
        list[TaskSettings], Field(min_length=1, description="The scraper tasks the bot will have to perform")
    ]
    notifications: Annotated[NotificationsSettings, Field(description="Notifications configuration")]
    redis: Annotated[RedisDsn, Field(description="An URI to a redis instance used to cache")]

    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="SB__",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    _SETTINGS_PATH: ClassVar[str | Path | list[str | Path]] = DEFAULT_SETTINGS_PATH

    @classmethod
    def set_settings_path(cls, settings_path: str | Path | list[str | Path]) -> None:
        cls._SETTINGS_PATH = settings_path

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        **kwargs
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls, yaml_file=cls._SETTINGS_PATH),
        )

    # Make the first initialization persistence
    # between multiple initialization of the class
    _instance: ClassVar[Self | None] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        if not self.__class__._initialized:
            super().__init__(**kwargs)
            self.__class__._initialized = True
