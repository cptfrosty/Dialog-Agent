from qdrant_client import QdrantClient
from llm.gigachat_client import GigaChatClient
from vector_db.qdrant_manager import QdrantManager


class Agent:
    def __init__(self):
        self.gigachat_client = GigaChatClient()
        self.qdrant_manager = QdrantManager()

    def say(self, message):
        print(f"[Agent] Received: {message}")
        
        # Получаем контекст из Qdrant
        context = self.qdrant_manager.search_relevant_info(message)
        
        # Генерируем ответ с помощью GigaChat
        answer = self.gigachat_client.ask(context, message)
        
        print(f"[Agent] Final answer: {answer}")
        return answer


