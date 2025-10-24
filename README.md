# Dialog-Agent
[Dev] Диалоговый агент


## Модули
pydantic_settings - модуль библиотеки Pydantic для удобной работы с настройками приложения в Python-проектах. 
Он позволяет автоматически загружать настройки из переменных окружения, .env-файлов, словарей и других источников в виде Pydantic-моделей — с валидацией, аннотациями типов и автозаполнением в IDE

## Конфиг
```python
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
```
