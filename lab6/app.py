import os
from flask import Flask, jsonify
from database import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from repositories import UserRepository
from services import UserService
from handlers import UserHandler, user_bp, auth_bp

def create_app():
    app = Flask(__name__)

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError("Переменная окружения DATABASE_URL не задана!")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-default-key')

    # Инициализация расширений
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # Сборка приложения (Dependency Injection)
    repository = UserRepository()
    service = UserService(repository)
    handler = UserHandler(service)
    handler.register_routes()

    # Регистрация Blueprint'ов
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"status": "error", "code": 500, "message": "Внутренняя ошибка сервера"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)