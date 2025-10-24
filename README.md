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
## Последовательность работы системы
**1. Инициализация:**

```python
# Запуск всех компонентов
bot = TelegramBot(token="YOUR_BOT_TOKEN")
qdrant = QdrantManager(host="localhost")
aitunnel = AITunnelClient(api_key="YOUR_AITUNNEL_KEY")
agent = DialogAgent(qdrant, aitunnel)
```

**2. Обработка сообщения:**

- Пользователь отправляет сообщение в Telegram

- Бот передает сообщение в DialogAgent

- Агент определяет интент (вопрос/рекомендация)

- Соответствующий модуль обрабатывает запрос

- Формируется и возвращается ответ

**3. RAG-процесс:**

- Векторизация вопроса → поиск в Qdrant → генерация ответа через AiTunnel

**4. Рекомендации:**

- Анализ профиля + запроса → поиск материалов → форматирование ответа
