CONFIG_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "scraper_bot/config.schema.json",
    "title": "Scraper bot configuration",
    "type": "object",
    "properties": {
        "bot": {
            "type": "object",
            "properties": {
                "token": {"type": "string"},
                "chats": {
                    "type": "array",
                    "items": [{"type": "integer"}, {"type": "integer"}],
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
