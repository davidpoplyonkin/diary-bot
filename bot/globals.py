import os

# Bot
TG_TOKEN=os.environ.get("TG_TOKEN")
ADMIN_TG_ID=os.environ.get("ADMIN_TG_ID")
COMMANDS=[
    {
        "command": "/start",
        "description": "Почати першу розмову з ботом"
    }, {
        "command": "/help",
        "description": "Переглянути повний список доступних команд"
    }, {
        "command": "/enter",
        "description": "Внести дані"
    }, {
        "command": "/notifications",
        "description": "Налаштування нагадувань"
    }
]
TZ=os.environ.get("TZ")
HEALTH_METRICS = {
    "sbpm": {
        "name": "Систолічний кров’яний тиск",
        "first": True,
        "button_text": "Тиск (ранок)",
        "prompt": "Введіть свій систолічний кров’яний тиск:",
        "next": "dbpm", 
    },
    "dbpm": {
        "name": "Діастолічний кров’яний тиск",
        "prompt": "Введіть свій діастолічний кров’яний тиск:",
        "next": "pm",
    },
    "pm": {
        "name": "Пульс",
        "prompt": "Введіть свій пульс:",
    },
    "sbpe": {
        "name": "Систолічний кров’яний тиск",
        "first": True,
        "button_text": "Тиск (вечір)",
        "prompt": "Введіть свій систолічний кров’яний тиск:",
        "next": "dbpe", 
    },
    "dbpe": {
        "name": "Діастолічний кров’яний тиск",
        "prompt": "Введіть свій діастолічний кров’яний тиск:",
        "next": "pe",
    },
    "pe": {
        "name": "Пульс",
        "prompt": "Введіть свій пульс:",
    },
    "weight": {
        "name": "Вага",
        "first": True,
        "button_text": "Вага",
        "prompt": "Введіть свою вагу (кг):"
    },
    "glf": {
        "name": "Глюкоза (натще)",
        "first": True,
        "button_text": "Глюкоза (натще)",
        "prompt": "Введіть свій рівень глюкози натще:"
    },
    "glp": {
        "name": "Глюкоза (після їжі)",
        "first": True,
        "button_text": "Глюкоза (після їжі)",
        "prompt": "Введіть свій рівень глюкози після їжі:"
    },
    "ttr": {
        "name": "Тестостерон",
        "first": True,
        "button_text": "Тестостерон",
        "prompt": "Введіть свій рівень тестостерона:"
    }
}

# Postgres
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_USER = os.environ.get("POSTGRES_USER")

# Dashboard
DASHBOARD_URL = os.environ.get("DASHBOARD_URL")
