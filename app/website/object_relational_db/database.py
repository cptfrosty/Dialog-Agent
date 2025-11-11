# database.py
import hashlib
import secrets
from datetime import datetime, timedelta

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