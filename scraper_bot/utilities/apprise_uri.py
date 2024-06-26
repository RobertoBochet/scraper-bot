from typing import ClassVar

from apprise import Apprise
from pydantic import SecretStr
from pydantic_core import CoreSchema
from pydantic_core.core_schema import no_info_after_validator_function, str_schema


def _validate_apprise_uri(v: str) -> str:
    if Apprise.instantiate(v) is None:
        raise ValueError("Invalid Apprise URI")
    return v


class SecretAppriseUri(SecretStr, str):
    _inner_schema: ClassVar[CoreSchema] = no_info_after_validator_function(_validate_apprise_uri, str_schema())
    _error_kind: ClassVar[str] = "string_type"

    def _display(self) -> str:
        v = self.get_secret_value()
        i, j = len(v) // 6, len(v) * 5 // 6
        return f"{v[:i]}*****{v[j:]}"
