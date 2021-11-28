import logging
from typing import Callable

import requests
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__package__)


class Scraper:
    url: str
    target: str
    on_find: Callable[[...], None]

    def __init__(self, url: str, target: str, on_find: Callable[[...], None]):
        self.url = url
        self.target = target
        self.on_find = on_find

    def run(self):
        _LOGGER.info(f"Start scraping {self.url}")

        entities = []
        last_page_entities = []

        i = 0
        while True:
            i += 1
            url = self.url.replace("{i}", f"{i}")

            _LOGGER.info(f"Get page {url}")

            page = requests.get(url)

            if not page.ok:
                break

            soup = BeautifulSoup(page.text, "html.parser")

            page_entities = soup.select(self.target)

            if len(page_entities) == 0:
                break

            page_entities = [e["href"] for e in page_entities]

            # some site given a pagination greater than
            # the last page return the last page
            # if all links are identical between
            # two consequential pages then break
            # this is a WA to handle this situation
            if (
                len(page_entities) == len(last_page_entities)
                and len(
                    [
                        1
                        for i, j in zip(page_entities, last_page_entities)
                        if i != j
                    ]
                )
                == 0
            ):
                break

            _LOGGER.info(
                f"Found {len(page_entities)} entries in the current page"
            )

            entities += page_entities
            last_page_entities = page_entities

        _LOGGER.info(f"Found {len(entities)} entries")

        self.on_find(*entities)

        _LOGGER.info(f"Scraping {self.url} completed")
