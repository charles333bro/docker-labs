import os
from flask import Flask, jsonify
from database import db
from repositories import UserRepository
from services import UserService
from handlers import UserHandler, user_bp

def create_app():
    app = Flask(__name__)

    # Конфигурация через переменные окружения
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError("Переменная окружения DATABASE_URL не задана!")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация БД
    db.init_app(app)

    # --- Dependency Injection (Сборка приложения) ---
    repository = UserRepository()
    service = UserService(repository)
    handler = UserHandler(service)
    handler.register_routes()

    # Регистрация Blueprint
    app.register_blueprint(user_bp)

    # Создание таблиц при первом запуске (для простоты)
    with app.app_context():
        db.create_all()

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"status": "error", "code": 500, "message": "Внутренняя ошибка сервера"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)