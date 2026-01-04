from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class WhatsAppMessage(BaseModel):
    message_type: str  # 'text', 'image', etc.
    from_number: str
    text_body: Optional[str] = None
    timestamp: str

class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[Dict[str, Any]]