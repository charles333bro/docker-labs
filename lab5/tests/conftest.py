import pytest
import os
from app import create_app
from database import db as _db

@pytest.fixture(scope='session')
def app():
    # Подменяем переменную окружения для тестов (используем SQLite в памяти)
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Фикстура для отправки HTTP-запросов к API в тестах"""
    return app.test_client()