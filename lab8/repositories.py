from models import User, Record
from database import db
from sqlalchemy.orm import joinedload

class UserRepository:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_by_id(self, user_id):
        return db.session.get(User, user_id)

    def create(self, username, password, age=None):
        user = User(username=username, age=age)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    # РЕШЕНИЕ ПРОБЛЕМЫ N+1: загружаем пользователя и его записи ОДНИМ запросом
    def get_user_with_records(self, user_id):
        return db.session.query(User).options(joinedload(User.records)).filter(User.id == user_id).first()

class RecordRepository:
    def create(self, user_id, title, amount):
        record = Record(user_id=user_id, title=title, amount=amount)
        db.session.add(record)
        db.session.commit()
        return record

    def get_by_id(self, record_id):
        return db.session.get(Record, record_id)