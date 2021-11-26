import yaml
from ischedule import run_loop

from .task import Task


class BotScraper:
    tasks: list[Task]

    def __init__(self, bot: dict, tasks: list):
        self.tasks = [Task.make(c) for c in tasks]

    def _setup_tasks(self):
        for t in self.tasks:
            t.schedule()

    def start(self):
        self._setup_tasks()

        run_loop()

    @classmethod
    def make(cls, config: dict):
        return cls(**config)

    @classmethod
    def make_from_config(cls, config_file: str):
        with open(config_file) as f:
            return cls.make(yaml.safe_load(f))
