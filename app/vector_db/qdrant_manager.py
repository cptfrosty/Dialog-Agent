import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import numpy as np


class QdrantManager:
    def __init__(self, host, collection_name="test_db1"):
        # Инициализируем в конструкторе
        self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.client = QdrantClient(host, port=6333)
        self.collection_name = collection_name

    def search_relevant_info(self, query, top_k=5):
        """Поиск релевантной информации в Qdrant"""
        print(f"[Qdrant] Searching for: '{query}'")
        
        # Векторизация запроса
        query_vector = self.encoder.encode(query).tolist()
        
        # Поиск в Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=0.3
        )
        
        print(f"[Qdrant] Search returned {len(search_result)} results")
        
        # Сбор релевантных текстов
        context_parts = []
        for i, hit in enumerate(search_result):
            print(f"[Qdrant] Result {i}: score={hit.score:.3f}")
            print(f"[Qdrant] Payload keys: {list(hit.payload.keys())}")
            
            # Пытаемся найти текстовое содержимое
            text_content = self._extract_text_from_payload(hit.payload)
            
            if text_content:
                context_parts.append(text_content)
                print(f"  Text: {text_content[:80]}...")
            else:
                print(f"  No suitable text found in payload")
        
        context = "\n".join(context_parts)
        if not context:
            context = "Информация по вашему вопросу не найдена в базе знаний."
        
        print(f"[Qdrant] Final context: {len(context)} chars")
        return context
    
    def _extract_text_from_payload(self, payload):
        """Извлекает текст из payload разными способами"""
        # Способ 1: Если есть поле "text"
        if "text" in payload:
            return str(payload["text"])
        
        # Способ 2: Объединяем все строковые поля
        text_parts = []
        for key, value in payload.items():
            if isinstance(value, str) and value.strip():
                text_parts.append(value)
            elif pd.notna(value):  # Обработка числовых и других значений
                text_parts.append(str(value))
        
        if text_parts:
            return " ".join(text_parts)
        
        return None