import os
import threading
from telegram_bot import TelegramRunner
from dotenv import load_dotenv



def main():
    load_dotenv()
    bot = TelegramRunner()
    bot.start()
    

if __name__ == "__main__":
    main()