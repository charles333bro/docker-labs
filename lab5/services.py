class UserService:
    """Слой бизнес-логики (Business Logic Layer)."""

    def __init__(self, repository):
        # Внедрение зависимости (Dependency Injection)
        self.repository = repository

    def get_all_users(self):
        return self.repository.get_all()

    def get_user(self, user_id):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        return user

    def create_user(self, data):
        # Валидация (перенесена из lab3)
        if not data or 'name' not in data or 'age' not in data:
            raise ValueError("Поля 'name' и 'age' обязательны")
        
        name = data['name']
        age = data['age']

        if not isinstance(name, str) or len(name) < 3:
            raise ValueError("Имя должно быть строкой и содержать минимум 3 символа")
        if not isinstance(age, int) or not (1 <= age <= 120):
            raise ValueError("Возраст должен быть целым числом от 1 до 120")

        return self.repository.create(name, age)

    def update_user(self, user_id, data):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        name = data.get('name')
        age = data.get('age')
        
        # Валидация для обновления
        if name is not None and (not isinstance(name, str) or len(name) < 3):
            raise ValueError("Имя должно быть строкой и содержать минимум 3 символа")
        if age is not None and (not isinstance(age, int) or not (1 <= age <= 120)):
            raise ValueError("Возраст должен быть целым числом от 1 до 120")

        return self.repository.update(user, name, age)

    def delete_user(self, user_id):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        self.repository.delete(user)