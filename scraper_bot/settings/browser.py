from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator

BrowserType = Literal["firefox", "chromium", "webkit"]


class BrowserSettings(BaseModel):
    type: Annotated[
        BrowserType | list[BrowserType],
        Field(description="Browser to use with playwright", default=["firefox", "chromium", "webkit"]),
    ]
    stealthEnabled: Annotated[bool, Field(description="Enable stealth mode", default=False)]
    headless: Annotated[bool, Field(description="Enable headless mode", default=True)]

    @field_validator("type")
    @classmethod
    def browser_type_to_list(cls, v: BrowserType | list[BrowserType]) -> list[BrowserType]:
        if isinstance(v, list):
            return v
        return [v]
