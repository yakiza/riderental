import logging
from fastapi import FastAPI
from app.routes import webhook
from app.config import settings

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper()))

app = FastAPI(title="WhatsApp Business Bot", version="1.0.0")
app.include_router(webhook.router)