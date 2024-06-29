from scraper_bot.exceptions import ScraperBotError


class CacheError(ScraperBotError):
    pass


class CacheConnectionError(CacheError):
    pass
