from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Telegram
    telegram_bot_token: str
    admin_ids: list[int]
    
    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    
    # AiTunnel
    aitunnel_api_key: str = "key"
    aitunnel_base_url: str = "https://api.aitunnel.ru/v1"
    
    # Model settings
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_temperature: float = 0.7

settings = Settings()