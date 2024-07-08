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

from ..utilities.disk_cache_dsn import DiskCacheDsn
from .browser import BrowserSettings
from .notifications import NotificationsSettings
from .task import TaskSettings

DEFAULT_SETTINGS_PATH = [
    Path.cwd() / "config.yml",
    Path.cwd() / "config.yaml",
    "/etc/scraper-bot/config.yml",
    "/etc/scraper-bot/config.yaml",
]


class Settings(BaseSettings):
    interval: Annotated[
        timedelta | None,
        Field(
            gt=1,
            description="How often the tasks should be done, expressed in seconds. "
            "If the value provided is 0 the task will run only once.",
            default=None,
        ),
    ]

    browser: Annotated[BrowserSettings, Field(description="Browser to use with playwright", default=BrowserSettings())]

    tasks: Annotated[
        list[TaskSettings], Field(min_length=1, description="The scraper tasks the bot will have to perform")
    ]
    notifications: Annotated[NotificationsSettings, Field(description="Notifications configuration")]
    cache: Annotated[
        RedisDsn | DiskCacheDsn | None,
        Field(description="A DSN to a redis instance or diskcache folder used to cache", default=None),
    ]

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
