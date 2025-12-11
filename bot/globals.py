import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN=os.environ.get("TG_TOKEN")
ADMIN_TG_ID=os.environ.get("ADMIN_TG_ID")
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