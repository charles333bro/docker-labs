class UserService:
    def __init__(self, repository):
        self.repository = repository

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

        if self.repository.get_by_username(username):
            raise ValueError("Пользователь с таким именем уже существует")

        return self.repository.create(username, password, age)

    def authenticate_user(self, data):
        if not data or not data.get('username') or not data.get('password'):
            raise ValueError("Поля 'username' и 'password' обязательны")

        user = self.repository.get_by_username(data['username'])
        if not user or not user.check_password(data['password']):
            raise ValueError("Неверное имя пользователя или пароль")
        
        return user

    def get_user_profile(self, user_id):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        return user