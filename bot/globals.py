import os

# Bot
TG_TOKEN=os.environ.get("TG_TOKEN")
ADMIN_TG_ID=os.environ.get("ADMIN_TG_ID")
TZ=os.environ.get("TZ")
HEALTH_METRICS = {
    "sbp": {
        "name": "Systolic blood pressure",
        "first": True,
        "button_text": "Pressure",
        "prompt": "Enter your systolic blood pressure:",
        "next": "dbp", 
    },
    "dbp": {
        "name": "Diastolic blood pressure",
        "prompt": "Enter your diastolic blood pressure:",
        "next": "pulse",
    },
    "pulse": {
        "name": "Pulse",
        "prompt": "Enter your pulse:",
    },
    "weight": {
        "name": "Weight",
        "first": True,
        "button_text": "Weight",
        "prompt": "Enter your weight(kg):"
    }
}

# Postgres
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
