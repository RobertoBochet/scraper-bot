from collections.abc import Collection
from typing import TYPE_CHECKING, Iterator

from .scraper_task_result_entity import ScraperTaskResultEntity

if TYPE_CHECKING:
    from .scraper_task import ScraperTask


class ScraperTaskResult(Collection):
    def __init__(self, task: "ScraperTask", data: list[dict]):
        self._task = task
        self._data = [ScraperTaskResultEntity(d, task=task) for d in data]

    @property
    def task(self) -> "ScraperTask":
        return self._task

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> ScraperTaskResultEntity:
        return self._data[index]

    def __iter__(self) -> Iterator[ScraperTaskResultEntity]:
        return self._data.__iter__()

    def __contains__(self, item) -> bool:
        return item in self._data
