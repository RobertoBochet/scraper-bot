CONFIG_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://scraper_bot.org/config.schema.json",
    "title": "Scraper bot configuration",
    "type": "object",
    "properties": {
        "bot": {
            "description": "Telegram bot configuration",
            "type": "object",
            "properties": {
                "token": {
                    "description": "The bot token provided by @BotFather",
                    "type": "string",
                    "pattern": "^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$",
                },
                "chats": {
                    "description": "It is a list of user_id or group_id "
                    "where the scraped entities will have to be sent",
                    "type": "array",
                    "items": {"type": "integer"},
                },
            },
            "required": ["token", "chats"],
        },
        "tasks": {
            "type": "array",
            "minItems": 1,
            "items": {"$ref": "#/$defs/Task"},
        },
        "redis": {
            "description": "An URI to a redis instance. "
            "Alternatively you can set it as environment variable `RS_REDIS`",
            "type": "string",
        },
    },
    "$defs": {
        "Task": {
            "type": "object",
            "properties": {
                "name": {
                    "description": "A human readable label for teh task",
                    "type": "string",
                },
                "url": {
                    "description": "The url to the page to be scraped. "
                    "Use `{i}` as a placeholder for the pagination",
                    "type": "string",
                },
                "target": {
                    "description": "It is a unique css selector to target "
                    "the <a> tag contains the link to the scraped page",
                    "type": "string",
                },
                "interval": {
                    "description": "How often the task should be done expressed in seconds",
                    "type": "integer",
                    "exclusiveMinimum": 0,
                },
            },
            "required": ["name", "url", "target", "interval"],
        }
    },
    "required": ["bot", "tasks"],
}
