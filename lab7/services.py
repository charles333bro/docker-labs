from database import db
from sqlalchemy.orm.exc import StaleDataError

class UserService:
    def __init__(self, user_repository):
        self.user_repo = user_repository

    def register_user(self, data):
        if not data or not data.get('username') or not data.get('password'):
            raise ValueError("Поля 'username' и 'password' обязательны")
        
        username = data['username']
        password = data['password']
        age = data.get('age')

        if len(username) < 3:
            raise ValueError("Имя пользователя должно содержать минимум 3 символа")
        if len(password) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")

        if self.user_repo.get_by_username(username):
            raise ValueError("Пользователь с таким именем уже существует")

        return self.user_repo.create(username, password, age)

    def authenticate_user(self, data):
        if not data or not data.get('username') or not data.get('password'):
            raise ValueError("Поля 'username' и 'password' обязательны")

        user = self.user_repo.get_by_username(data['username'])
        if not user or not user.check_password(data['password']):
            raise ValueError("Неверное имя пользователя или пароль")
        
        return user

    def get_user_profile(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        return user

class RecordService:
    def __init__(self, record_repo, user_repo):
        self.record_repo = record_repo
        self.user_repo = user_repo

    def create_record(self, user_id, title, amount):
        if not self.user_repo.get_by_id(user_id):
            raise ValueError("Пользователь не найден")
        return self.record_repo.create(user_id, title, amount)

    def update_record_amount(self, record_id, new_amount):
        record = self.record_repo.get_by_id(record_id)
        if not record:
            raise ValueError("Запись не найдена")
        
        record.amount = new_amount
        
        try:
            db.session.commit() # Транзакция завершается здесь
        except StaleDataError:
            db.session.rollback() # Откатываем транзакцию при конфликте
            raise ValueError("Конфликт! Данные были изменены другим пользователем. Попробуйте снова.")
        
        return record