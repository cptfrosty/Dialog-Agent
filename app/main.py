import os
import threading
from rag.engine import RagEngine
from telegram_bot import TelegramBotClient
from vector_db.qdrant_manager import QdrantManager
from llm.gigachat_client import GigaChatClient
from dotenv import load_dotenv

def run_bot():
    """Функция для запуска бота в отдельном потоке"""
    try:
        qdrant = QdrantManager(host=os.getenv("QDRANT_HOST"))
        gigachat = GigaChatClient(api_key=os.getenv("GIGACHAT_API_KEY"))
        rag = RagEngine(qdrant=qdrant, gigachat=gigachat)
        bot = TelegramBotClient(
            token=os.getenv("TELEGRAM_BOT_TOKEN"), 
            gigachat=gigachat, 
            qdrant=qdrant, 
            rag=rag
        )
        
        # Запускаем бота
        bot.run()  # или bot.start()
        
    except Exception as e:
        print(f"❌ Ошибка в потоке бота: {e}")
        import traceback
        traceback.print_exc()

def main():
    load_dotenv()
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, name="TelegramBot")
    bot_thread.daemon = True
    bot_thread.start()
    
    print("✅ Телеграм бот запущен в отдельном потоке")
    print("🚀 Позже здесь можно запустить веб-сервер")
    print("⏹️  Нажмите Ctrl+C для остановки")
    
    # Основной поток ждет
    try:
        while True:
            # Проверяем, жив ли поток с ботом
            if not bot_thread.is_alive():
                print("❌ Поток с ботом остановился, перезапускаем...")
                bot_thread = threading.Thread(target=run_bot, name="TelegramBot")
                bot_thread.daemon = True
                bot_thread.start()
                print("✅ Бот перезапущен")
            
            # Ждем немного перед следующей проверкой
            threading.Event().wait(10)  # Увеличил интервал проверки
            
    except KeyboardInterrupt:
        print("\n👋 Завершение работы...")

if __name__ == "__main__":
    main()