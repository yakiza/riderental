from fastapi import APIRouter, Request,Query, Response, status

from app.config import settings
from app.models.whatsapp import WhatsAppWebhookPayload
from app.services.whatsapp import WhatsAppClient
from app.services.message_handler import MessageHandler
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def parse_whatsapp_message(payload: dict) -> list:
    """Extract messages from webhook payload."""
    messages = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            if "messages" in value:
                for msg in value["messages"]:
                    if msg["type"] == "text":
                        messages.append(
                            WhatsAppMessage(
                                message_type="text",
                                from_number=msg["from"],
                                text_body=msg["text"]["body"],
                                timestamp=msg["timestamp"],
                            )
                        )
    return messages
@router.get("/webhook")
async def verify_webhook(
        hub_mode: str = Query(None, alias="hub.mode"),
        hub_verify_token: str = Query(None, alias="hub.verify_token"),
        hub_challenge: str = Query(None, alias="hub.challenge"),
):
    logger.info(f"Webhook verification attempt: mode={hub_mode}, token={hub_verify_token}")

    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return PlainTextResponse(content=hub_challenge)

    logger.warning("Webhook verification failed: invalid token or mode")
    return Response(status_code=status.HTTP_403_FORBIDDEN)

@router.post("/webhook")
async def handle_webhook(request: Request):
    payload: dict = await request.json()
    logger.debug(f"Received webhook: {json.dumps(payload, indent=2)}")

    # Initialize services (could be injected via DI in larger apps)
    client = WhatsAppClient(
        access_token=settings.WHATSAPP_ACCESS_TOKEN,
        phone_number_id=settings.WHATSAPP_PHONE_NUMBER_ID,
    )
    handler = MessageHandler(client=client)

    messages = parse_whatsapp_message(payload)
    for msg in messages:
        await handler.handle_message(msg)

    return {"status": "ok"}