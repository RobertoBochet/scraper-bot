from datetime import timedelta
from logging import getLogger
from typing import Annotated, Any

from pydantic import BaseModel, Field, HttpUrl, PositiveInt, model_validator


class TaskSettings(BaseModel):
    name: Annotated[str, Field(description="A human readable label for teh task")]
    url: Annotated[HttpUrl, Field(description="The url to the page to be scraped")]

    script: Annotated[
        str,
        Field(
            description="Javascript script to retrieve the target entities. "
            "The script have to return a object(dict) or a list of them. "
            "The attributes of the object will be accessible in the notification message template"
        ),
    ]
    target: Annotated[
        str | None,
        Field(
            deprecated=True,
            description="'target' is deprecated, use 'script' instead. "
            "Javascript script to retrieve the target entities. "
            "The script have to return a object(dict) or a list of them. "
            "The attributes of the object will be accessible in the notification message template",
            default=None,
        ),
    ]
    waitingForTarget: Annotated[
        str | None, Field(description="CSS selector for a target to wait before start the scraping", default=None)
    ]
    waitingTimeout: Annotated[
        timedelta,
        Field(description="The time to wait to get find the `waitingForTarget` before give up", default=15, ge=0),
    ]
    nextPageTarget: Annotated[
        str | None,
        Field(
            description="Javascript script to retrieve the next page url. "
            "The script have to return the url as a string",
            default=None,
        ),
    ]
    maxPages: Annotated[
        PositiveInt | None, Field(description="The maximum number of pages to scrape per task", default=None)
    ]

    @model_validator(mode="before")
    @classmethod
    def retro_compatibility(cls, values: dict[str, Any]) -> dict[str, Any]:
        if (target := values.get("target")) is not None:
            getLogger(__package__).warning("'target' is deprecated, use 'script' instead")
            if values.get("script") is None:
                values["script"] = target

        return values
