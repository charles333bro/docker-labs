from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer, nullable=True)

    # Связь один-ко-многим (для joinedload)
    records = db.relationship('Record', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "age": self.age}

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    
    # Поле для оптимистичной блокировки
    version = db.Column(db.Integer, nullable=False, default=1)

    # Включаем оптимистичную блокировку
    __mapper_args__ = {"version_id_col": version}

    # Составной индекс для оптимизации запросов
    __table_args__ = (
        Index('ix_records_user_amount', 'user_id', 'amount'),
    )

    def to_dict(self):
        return {
            "id": self.id, 
            "user_id": self.user_id, 
            "title": self.title, 
            "amount": self.amount, 
            "version": self.version
        }