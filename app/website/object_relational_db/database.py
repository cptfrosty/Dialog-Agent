# database.py
import hashlib
import json
import os
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

class DataBase:
    def __init__(self):

        load_dotenv()

        print("PGSQL_HOST:", os.getenv("PGSQL_HOST"))
        print("PGSQL_PORT:", os.getenv("PGSQL_PORT")) 
        print("PGSQL_USER:", os.getenv("PGSQL_USER"))
        print("PGSQL_PASSWORD:", "***" if os.getenv("PGSQL_PASSWORD") else "NOT SET")

        try:
            
            connection = self.create_connection_db()
            # Создание курсора
            cur = connection.cursor()
            
            # Выполнение запроса
            cur.execute("SELECT version();")
            
            # Получение результата
            version = cur.fetchone()
            print(f"PostgreSQL version: {version[0]}")

            connection.close()

        except Exception as error:
            print(f"Ошибка подключение к PGSQL: {error}")

    def create_connection_db(self):
        """Создание подключения к базе данных"""
        try:
            connection = psycopg2.connect(
                host = os.getenv("PGSQL_HOST"),
                port = os.getenv("PGSQL_PORT"),
                user = os.getenv("PGSQL_USER"),
                password = os.getenv("PGSQL_PASSWORD"),
                dbname = os.getenv("PGSQL_DATABASE"),
                # port - указывается самостоятельно
            )

            return connection
        except Exception as error:
            print(f"Ошибка подключение к PGSQL: {error}")
            return None

    def create_user(self, email, password, firstname, lastname, phone):
        """Создание нового пользователя"""
        connection = self.create_connection_db()

        try:
            with connection.cursor() as cursor:
                # Шифрование пароля
                password_hash, salt = self.hash_password(password=password, salt='agent')
                
                # Вызываем функцию PostgreSQL
                cursor.callproc('create_user_check', [
                    email,                   # p_email
                    password_hash,           # p_password_hash
                    "student",               # p_role
                    firstname,               # p_first_name
                    lastname,                # p_last_name
                    phone,                   # p_phone
                    "none",                  # p_avatar_url
                    True,                    # p_is_active
                    datetime.now(),          # p_created_at
                    datetime.now(),          # p_updated_at
                    datetime.now(),          # p_last_login
                    datetime.now()           # p_last_activity
                ])

                    
                # Получаем результат (true/false)
                result = cursor.fetchone()[0]
                connection.commit()
                
                if isinstance(result, str):
                    result = json.loads(result)

                if result['success']:
                    print(f"Success: {result['message']}")
                    print(f"User ID: {result['user_id']}")
                else:
                    print(f"Error: {result['message']}")
                    print(f"Error code: {result['error_code']}")

                connection.close()
                cursor.close()

                return result['success'], result['message']
                    
        except Exception as e:
            connection.rollback()
            print(f"Ошибка при вызове функции: {e}")
            return False

    def verify_user(self, email, password):
        """Проверка логина и пароля"""
        
        connection = self.create_connection_db()

        try:
            with connection.cursor() as cursor:
                # Шифрование пароля
                password_hash, salt = self.hash_password(password=password, salt='agent')
                
                # Вызываем функцию PostgreSQL
                cursor.callproc('verify_user_check', [
                    email,                   # p_email
                    password_hash,           # p_password_hash
                ])

                # Получаем результат (true/false)
                result = cursor.fetchone()[0]
                
                if isinstance(result, str):
                    result = json.loads(result)

                if result['success']:
                    print(f"Success: {result['message']}")
                    print(f"User ID: {result['user_id']}")
                    print(f"Role: {result['role']}")
                    print(f"Is_active {result['is_active']}")
                else:
                    print(f"Error: {result['message']}")
                    print(f"Error code: {result['error_code']}")

                connection.close()
                cursor.close()

                return result['success'], result['message'], result['lastname'], result['firstname']
                    
        except Exception as e:
            connection.rollback()
            print(f"Ошибка при вызове функции: {e}")
            return False

    def hash_password(self, password, salt=None):
        """Хеширование пароля с солью"""
        if salt is None:
            salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return password_hash, salt     


class AuthDatabaseMock:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.next_user_id = 1
        self._create_test_user()
    
    def _create_test_user(self):
        """Создает тестового пользователя для демонстрации"""
        test_password = "123456"
        password_hash, salt = self.hash_password(test_password)
        
        self.users["demo"] = {
            "id": self.next_user_id,
            "username": "demo",
            "password_hash": password_hash,
            "salt": salt,
            "created_at": datetime.now(),
            "is_active": True
        }
        self.next_user_id += 1
    
    def hash_password(self, password, salt=None):
        """Хеширование пароля с солью"""
        if salt is None:
            salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return password_hash, salt
    
    def create_user(self, username, password):
        """Создание нового пользователя"""
        if username in self.users:
            return False  # Пользователь уже существует
        
        password_hash, salt = self.hash_password(password)
        
        self.users[username] = {
            "id": self.next_user_id,
            "username": username,
            "password_hash": password_hash,
            "salt": salt,
            "created_at": datetime.now(),
            "is_active": True
        }
        self.next_user_id += 1
        return True
    
    def verify_user(self, username, password):
        """Проверка логина и пароля"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        if not user["is_active"]:
            return None
        
        stored_hash = user["password_hash"]
        salt = user["salt"]
        input_hash, _ = self.hash_password(password, salt)
        
        if stored_hash == input_hash:
            return user["id"]
        return None
    
    def create_session(self, user_id):
        """Создание сессии"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        
        self.sessions[session_token] = {
            "user_id": user_id,
            "expires_at": expires_at
        }
        return session_token
    
    def validate_session(self, session_token):
        """Проверка валидности сессии"""
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        if session["expires_at"] < datetime.now():
            del self.sessions[session_token]  # Удаляем просроченную сессию
            return None
        
        # Находим username по user_id
        user_id = session["user_id"]
        for username, user_data in self.users.items():
            if user_data["id"] == user_id:
                return (user_id, username)
        
        return None
    
    def delete_session(self, session_token):
        """Удаление сессии (выход)"""
        if session_token in self.sessions:
            del self.sessions[session_token]
    
    def get_stats(self):
        """Получение статистики системы"""
        return {
            "total_users": len(self.users),
            "active_sessions": len(self.sessions)
        }