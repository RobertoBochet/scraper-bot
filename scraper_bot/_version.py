from importlib import metadata

try:
    __version__ = metadata.version("scraper-bot")
except ImportError:
    __version__ = "0.dev"
