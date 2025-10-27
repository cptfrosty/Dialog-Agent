import os
from core.agent import Agent
from llm.gigachat_client import GigaChatClient  # Прямой импорт из файла
from dotenv import load_dotenv

def main():
    load_dotenv()
    agent = Agent()
    agent.say("Я потерял студенческий билет, что делать?")


if __name__ == "__main__":
    main()