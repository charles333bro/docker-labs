from models import User
from database import db

class UserRepository:
    """Слой для работы с базой данных (Data Access Layer)."""

    def get_all(self):
        return User.query.all()

    def get_by_id(self, user_id):
        return db.session.get(User, user_id)

    def create(self, name, age):
        user = User(name=name, age=age)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user, name, age):
        if name is not None:
            user.name = name
        if age is not None:
            user.age = age
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()