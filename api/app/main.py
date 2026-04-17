from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv("../.env")

from .routers import router_auth, router_user, router_health_metric
from .globals import API_ALLOW_ORIGINS


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_health_metric)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
