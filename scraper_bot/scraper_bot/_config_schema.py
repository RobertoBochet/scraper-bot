CONFIG_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://scraper_bot.org/config.schema.json",
    "title": "Scraper bot configuration",
    "type": "object",
    "properties": {
        "bot": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "pattern": "^[0-9]{10}:[a-zA-Z0-9_-]{35}$",
                },
                "chats": {
                    "type": "array",
                    "items": {"type": "integer"},
                },
            },
            "required": ["token", "chats"],
        },
        "tasks": {"type": "array", "items": {"$ref": "#/$defs/Task"}},
        "redis": {"type": "string"},
    },
    "$defs": {
        "Task": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "url": {"type": "string"},
                "target": {"type": "string"},
                "interval": {"type": "integer"},
            },
            "required": ["name", "url", "target", "interval"],
        }
    },
    "required": ["bot", "tasks"],
}
