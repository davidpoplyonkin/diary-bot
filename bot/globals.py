import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN=os.environ.get("TG_TOKEN")
ADMIN_TG_ID=os.environ.get("ADMIN_TG_ID")