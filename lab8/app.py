import os
from flask import Flask, jsonify
from database import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from repositories import UserRepository, RecordRepository
from services import UserService, RecordService
from handlers import UserHandler, user_bp, auth_bp, record_bp

def create_app():
    app = Flask(__name__)

    # --- НАСТРОЙКА CORS (Разрешаем запросы только нашему фронтенду) ---
    # В реальном проекте здесь будет URL твоего сайта, например: origins=["https://my-site.com"]
    CORS(app, resources={r"/*": {"origins": "*"}}) 

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError("Переменная окружения DATABASE_URL не задана!")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-default-key')

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # --- DEPENDENCY INJECTION ---
    user_repo = UserRepository()
    record_repo = RecordRepository()
    
    user_service = UserService(user_repo)
    record_service = RecordService(record_repo, user_repo)
    
    handler = UserHandler(user_service, record_service, user_repo)
    handler.register_routes()

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(record_bp)

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"status": "error", "code": 500, "message": "Внутренняя ошибка сервера"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    # ВАЖНО: При работе через Nginx (reverse proxy) Flask лучше запускать на порту 5000
    app.run(host='0.0.0.0', port=5000)