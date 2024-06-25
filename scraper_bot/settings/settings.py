from datetime import timedelta
from pathlib import Path
from typing import Annotated, ClassVar, Literal, Self, Type
from uuid import uuid4

from apprise import NOTIFY_FORMATS, NotifyFormat
from jinja2 import BaseLoader, Environment, Template
from pydantic import BaseModel, Field, HttpUrl, PrivateAttr, RedisDsn, model_validator
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from scraper_bot.utilities.AppriseURI import SecretAppriseUri

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


class NotificationChannel(BaseModel):
    title: Annotated[str | None, Field(description="The title of the notification", default=None)]
    message: Annotated[str | None, Field(description="The message of the notification", default=None)]
    format: Annotated[
        Literal[NOTIFY_FORMATS] | None, Field(description="The format of the notification message", default=None)
    ]
    uri: Annotated[SecretAppriseUri, Field(description="The URI of the notification")]

    _tag: Annotated[str, PrivateAttr(default_factory=lambda: uuid4().hex)]

    @property
    def tag(self) -> str:
        return self._tag

    _jinja_env: ClassVar[Environment] = Environment(loader=BaseLoader(), autoescape=True)

    @property
    def message_template(self) -> Template:
        return NotificationChannel._jinja_env.from_string(self.message)


class NotificationsSettings(BaseSettings):
    title: Annotated[str, Field(description="Title of the notification", default="New entry found")]
    message: Annotated[
        str, Field(description="The message of the notification", default="New entry found [here]({{url}})")
    ]
    format: Annotated[
        Literal[NOTIFY_FORMATS], Field(description="The format of the notification message", default=NotifyFormat.TEXT)
    ]
    channels: Annotated[
        list[SecretAppriseUri | NotificationChannel],
        Field(description="Notification channel or apprise compatible URI", min_length=1),
    ]

    @model_validator(mode="after")
    def parse_channels(self) -> Self:
        self.channels = [
            NotificationChannel(
                **{
                    **self.model_dump(),
                    **(c.model_dump(exclude_none=True) if isinstance(c, NotificationChannel) else {"uri": c}),
                }
            )
            for c in self.channels
        ]
        return self


class Settings(BaseSettings):
    tasks: Annotated[list[Task], Field(min_length=1)]
    notifications: Annotated[NotificationsSettings, Field(description="Notifications configuration")]
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
