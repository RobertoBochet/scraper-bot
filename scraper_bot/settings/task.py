from datetime import timedelta
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl, PositiveInt


class TaskSettings(BaseModel):
    name: Annotated[str, Field(description="A human readable label for teh task")]
    url: Annotated[HttpUrl, Field(description="The url to the page to be scraped")]

    target: Annotated[
        str,
        Field(
            description="Javascript script to retrieve the target entities. "
            "The script have to return a object(dict) or a list of them. "
            "The attributes of the object will be accessible in the notification message template"
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
