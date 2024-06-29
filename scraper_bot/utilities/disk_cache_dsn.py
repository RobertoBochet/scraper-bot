from typing import Annotated

from pydantic import AfterValidator, UrlConstraints
from pydantic_core import Url


def _check_must_none_fields(v: Url) -> Url:
    for f in ["host", "port", "query", "fragment", "username", "password"]:
        if v.__getattribute__(f) is not None:
            raise ValueError(f"{f} is not allowed")
    return v


DiskCacheDsn = Annotated[Url, UrlConstraints(allowed_schemes=["diskcache"]), AfterValidator(_check_must_none_fields)]
