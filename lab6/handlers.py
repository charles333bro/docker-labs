from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('users', __name__)
auth_bp = Blueprint('auth', __name__)

class UserHandler:
    def __init__(self, service):
        self.service = service

    def register_routes(self):
        # --- Аутентификация ---
        @auth_bp.route('/register', methods=['POST'])
        def register():
            data = request.get_json()
            try:
                user = self.service.register_user(data)
                return jsonify(user.to_dict()), 201
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 400

        @auth_bp.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            try:
                user = self.service.authenticate_user(data)
                # Создаем JWT токен, в identity кладем ID пользователя
                access_token = create_access_token(identity=str(user.id))
                return jsonify({"access_token": access_token}), 200
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 401

        # --- Профиль (Защищенный эндпоинт) ---
        @user_bp.route('/profile', methods=['GET'])
        @jwt_required()  # Этот декоратор требует наличия валидного токена
        def get_profile():
            current_user_id = get_jwt_identity() # Достаем ID из токена
            try:
                user = self.service.get_user_profile(int(current_user_id))
                return jsonify(user.to_dict()), 200
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 404