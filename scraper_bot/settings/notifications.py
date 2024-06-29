from functools import cached_property
from typing import Annotated, ClassVar, Literal, Self
from uuid import uuid4

from aiolimiter import AsyncLimiter
from apprise import NOTIFY_FORMATS, NotifyFormat
from jinja2 import BaseLoader, Environment, Template
from pydantic import BaseModel, Field, PrivateAttr, model_validator

from scraper_bot.utilities.apprise_uri import SecretAppriseUri

Format = Literal[NOTIFY_FORMATS]


class NotificationChannel(BaseModel):
    title: Annotated[str | None, Field(description="The title of the notification", default=None)]
    message: Annotated[str | None, Field(description="The message of the notification", default=None)]
    format: Annotated[Format | None, Field(description="The format of the notification message", default=None)]
    uri: Annotated[SecretAppriseUri, Field(description="The URI of the notification")]
    rateLimit: Annotated[float | None, Field(description="Rate limit in messages per second", default=None, ge=1)]

    _tag: Annotated[str, PrivateAttr(default_factory=lambda: uuid4().hex)]

    @property
    def tag(self) -> str:
        return self._tag

    _jinja_env: ClassVar[Environment] = Environment(loader=BaseLoader(), autoescape=True)

    @property
    def message_template(self) -> Template:
        return NotificationChannel._jinja_env.from_string(self.message)

    @cached_property
    def rate_limiter(self) -> AsyncLimiter:
        return AsyncLimiter(self.rateLimit, time_period=1)


class NotificationsSettings(BaseModel):
    title: Annotated[str, Field(description="Title of the notification", default="")]
    message: Annotated[
        str, Field(description="The message of the notification", default="New entry found [here]({{url}})")
    ]
    format: Annotated[Format, Field(description="The format of the notification message", default=NotifyFormat.TEXT)]
    channels: Annotated[
        list[SecretAppriseUri | NotificationChannel],
        Field(description="Notification channel or apprise compatible URI", min_length=1),
    ]
    rateLimit: Annotated[float, Field(description="Rate limit in messages per second", default=10, ge=1)]

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
