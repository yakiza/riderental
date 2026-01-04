from typing import Protocol
from app.models.whatsapp import WhatsAppMessage

class IWhatsAppClient(Protocol):
    async def send_message(self, to: str, text: str) -> dict: ...

class MessageHandler:
    """Handles incoming WhatsApp messages and replies based on business logic."""
    def __init__(self, client: IWhatsAppClient):
        self.client = client

    async def handle_message(self, message: WhatsAppMessage) -> None:
        # Example: echo bot
        reply_text = f"You said: {message.text_body}. Thanks for messaging us!"
        await self.client.send_message(message.from_number, reply_text)