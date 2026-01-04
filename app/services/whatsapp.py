from abc import ABC, abstractmethod
import httpx
from app.config import settings

class IWhatsAppClient(ABC):
    @abstractmethod
    async def send_message(self, to: str, text: str) -> dict:
        pass

class WhatsAppClient(IWhatsAppClient):
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/v24.0/{phone_number_id}/messages"

    async def send_message(self, to: str, text: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "text": {"body": text},
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()