import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    """Load configuration from environment variables (12-Factor compliant)."""

    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    WHATSAPP_VERIFY_TOKEN: str = os.getenv("WHATSAPP_VERIFY_TOKEN")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    PORT: int = int(os.getenv("PORT", "8080"))

    def __post_init__(self) -> None:
        missing = [
            name for name, value in {
                "WHATSAPP_ACCESS_TOKEN": self.WHATSAPP_ACCESS_TOKEN,
                "WHATSAPP_PHONE_NUMBER_ID": self.WHATSAPP_PHONE_NUMBER_ID,
                "WHATSAPP_VERIFY_TOKEN": self.WHATSAPP_VERIFY_TOKEN,
            }.items()
            if not value
        ]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


settings = Settings()
