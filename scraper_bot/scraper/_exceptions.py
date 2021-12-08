class ScraperError(Exception):
    pass


class NoTargetFound(ScraperError):
    pass


class RequestError(ScraperError):
    pass
