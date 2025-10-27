# Dialog-Agent
[Dev] Диалоговый агент


## Модули
pydantic_settings - модуль библиотеки Pydantic для удобной работы с настройками приложения в Python-проектах. 
Он позволяет автоматически загружать настройки из переменных окружения, .env-файлов, словарей и других источников в виде Pydantic-моделей — с валидацией, аннотациями типов и автозаполнением в IDE

## Конфиг (.env)
```python
# Telegram
telegram_bot_token = ""
    
# Qdrant
qdrant_host = "localhost"
qdrant_port = 6333
    
# AiTunnel
aitunnel_api_key = "key"
aitunnel_base_url ="https://api.aitunnel.ru/v1"

# GigaChat
GIGACHAT_CLIENT_ID = "***client_id"
GIGACHAT_API_KEY = "***key"
gigachat_model = "GigaChat-2-Max"
gigachat_credentials = "200"
    
# Model settings
embedding_model = "all-MiniLM-L6-v2"
llm_temperature = 0.7
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
