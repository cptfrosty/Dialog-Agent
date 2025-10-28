from telegram.ext import Application, MessageHandler, filters
from core.agent import DialogAgent

class TelegramBotClient:
    def __init__(self, token: str, gigachat, qdrant, rag):
        self.token = token
        self.bot = Application.builder().token(self.token).build()
        self.agent = DialogAgent(gigachat, qdrant, rag)
        
        # Настраиваем обработчики при инициализации
        self._setup_handlers()

    def _setup_handlers(self):
        """Настройка обработчиков сообщений"""
        async def message_handler(update, context):
            message = update.message.text
            user = update.effective_user
            
            print(f"Новое сообщение от {user.username}: {message}")

            if "статус" in message.lower():
                await update.message.reply_text("Агент работает")
            else:
                response = self.agent.say(message)
                await update.message.reply_text(response)
        
        self.bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    def run(self):
        """Запуск бота (синхронный метод для использования в потоках)"""
        print("Бот запущен...")
        self.bot.run_polling()

    # Альтернативное название метода для ясности
    def start(self):
        """Альтернативное название для запуска"""
        self.run()