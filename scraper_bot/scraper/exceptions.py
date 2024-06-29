from scraper_bot.exceptions import ScraperBotError


class ScraperTaskError(ScraperBotError):
    pass


class TargetScriptError(ScraperTaskError):
    pass


class NoBrowserAvailable(ScraperTaskError):
    pass
