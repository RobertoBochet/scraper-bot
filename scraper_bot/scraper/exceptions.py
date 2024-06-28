class ScraperTaskError(Exception):
    pass


class TargetScriptError(ScraperTaskError):
    pass


class NoBrowserAvailable(ScraperTaskError):
    pass
