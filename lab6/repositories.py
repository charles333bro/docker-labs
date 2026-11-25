from models import User
from database import db

class UserRepository:
    def get_by_username(self, username):
        # ORM автоматически использует параметризованные запросы, защищая от SQL-инъекций
        return User.query.filter_by(username=username).first()

    def get_by_id(self, user_id):
        return db.session.get(User, user_id)

    def create(self, username, password, age=None):
        user = User(username=username, age=age)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user