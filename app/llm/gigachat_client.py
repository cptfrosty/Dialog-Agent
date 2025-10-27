''' 
Пример использования

load_dotenv()
giga_client = GigaChatClient()
print(giga_client.chat("Можно выучить программирование за 10 дней?"))
'''

from langchain_gigachat.chat_models import GigaChat
import os
from dotenv import load_dotenv

class GigaChatClient:
    def __init__(self):
        self.client_id = os.getenv("GIGACHAT_CLIENT_ID")
        self.api_key = os.getenv("GIGACHAT_API_KEY")
        self.model = os.getenv("gigachat_model")
        self.credentials = os.getenv("gigachat_credentials")

        self.llm = GigaChat(
            model=self.model,
            credentials=self.api_key,
            verify_ssl_certs=False
        )

    def chat(self, message):
        message = [{"role": "system", "content": "Ты супер позитивный помощник и всегда мотивируешь"},{"role": "user", "content": message}]
        response = self.llm.invoke(message)
        return response.content
    
    def ask(self, context, question):
        message = [
            {"role": "system", "content": "Ты - помощник студента. Отвечай на основе предоставленного контекста. Если в контексте нет информации, так и скажи."},
            {"role": "user", "content": f"Контекст: {context}\n\nВопрос: {question}"}
        ]
        
        try:
            response = self.llm.invoke(message)
            print(f"[GigaChat] Response type: {type(response)}")
            print(f"[GigaChat] Response attributes: {dir(response)}")
            
            # Для разных форматов ответа
            if hasattr(response, 'content'):
                print(f"[GigaChat] Using response.content")
                return response.content
            elif hasattr(response, 'text'):
                print(f"[GigaChat] Using response.text") 
                return response.text
            elif hasattr(response, 'choices') and len(response.choices) > 0:
                print(f"[GigaChat] Using response.choices[0].message.content")
                return response.choices[0].message.content
            else:
                print(f"[GigaChat] Fallback to str(response)")
                return str(response)
                
        except Exception as e:
            print(f"[GigaChat] Error: {e}")
            return "Извините, произошла ошибка при обработке вашего запроса."