import logging
from typing import Callable

import requests
from bs4 import BeautifulSoup

from ._exceptions import NoTargetFound, RequestError, ScraperError

_LOGGER = logging.getLogger(__package__)

_PAGE_PLACEHOLDER = "{i}"


class Scraper:
    url: str
    target: str
    on_find: Callable[[...], None]

    def __init__(self, url: str, target: str, on_find: Callable[[...], None]):
        self.url = url
        self.target = target
        self.on_find = on_find

    @property
    def is_multipage(self):
        return _PAGE_PLACEHOLDER in self.url

    def _scrape_page(self, url) -> list:
        _LOGGER.info(f"Get page {url}")

        page = requests.get(url)

        if not page.ok:
            raise RequestError

        soup = BeautifulSoup(page.text, "html.parser")

        page_entities = soup.select(self.target)

        if len(page_entities) == 0:
            raise NoTargetFound

        return [e["href"] for e in page_entities]

    def run(self):
        _LOGGER.info(f"Start scraping {self.url}")

        entities = []
        last_page_entities = []

        if self.is_multipage:
            i = 0
            while True:
                i += 1
                url = self.url.replace(_PAGE_PLACEHOLDER, f"{i}")

                _LOGGER.info(f"Get page {url}")

                try:
                    page_entities = self._scrape_page(url)
                except ScraperError:
                    break

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

        else:
            try:
                entities = self._scrape_page(self.url)
            except ScraperError:
                pass

        _LOGGER.info(f"Found {len(entities)} entries")

        self.on_find(*entities)

        _LOGGER.info(f"Scraping {self.url} completed")
