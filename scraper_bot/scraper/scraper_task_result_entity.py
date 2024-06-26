from collections.abc import Mapping
from hashlib import sha256
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scraper_task import ScraperTask


class ScraperTaskResultEntity(Mapping):
    def __init__(self, data: dict, task: "ScraperTask"):
        self._data = data
        self._task = task

    def __getitem__(self, item):
        if item == "task":
            return self._task
        return self._data[item]

    def __contains__(self, item):
        if item == "task":
            return True
        return item in self._data

    def __iter__(self):
        return iter({**self._data, "task": self._task})

    def __len__(self):
        return len(self._data) + 1

    def __str__(self) -> str:
        return f"{self._task.name}#{"|".join(["=".join(v) for v in sorted(self._data.items(), key=lambda x: x[0])])}"

    def __hash__(self) -> int:
        return int(sha256(str(self).encode()).hexdigest(), 16)

    @property
    def task(self) -> "ScraperTask":
        return self._task
