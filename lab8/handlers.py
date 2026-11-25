from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('users', __name__)
auth_bp = Blueprint('auth', __name__)
record_bp = Blueprint('records', __name__)

class UserHandler:
    def __init__(self, user_service, record_service, user_repo):
        self.user_service = user_service
        self.record_service = record_service
        self.user_repo = user_repo

    def register_routes(self):
        # --- АУТЕНТИФИКАЦИЯ ---
        @auth_bp.route('/register', methods=['POST'])
        def register():
            data = request.get_json()
            try:
                user = self.user_service.register_user(data)
                return jsonify(user.to_dict()), 201
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 400

        @auth_bp.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            try:
                user = self.user_service.authenticate_user(data)
                access_token = create_access_token(identity=str(user.id))
                return jsonify({"access_token": access_token}), 200
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 401

        # --- ПРОФИЛЬ ---
        @user_bp.route('/profile', methods=['GET'])
        @jwt_required()
        def get_profile():
            current_user_id = get_jwt_identity()
            try:
                user = self.user_service.get_user_profile(int(current_user_id))
                return jsonify(user.to_dict()), 200
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 404

        # --- ЗАПИСИ (ТРАНЗАКЦИИ И N+1) ---
        @record_bp.route('/records', methods=['POST'])
        @jwt_required()
        def create_record():
            current_user_id = int(get_jwt_identity())
            data = request.get_json()
            try:
                record = self.record_service.create_record(current_user_id, data['title'], data['amount'])
                return jsonify(record.to_dict()), 201
            except (KeyError, ValueError) as e:
                return jsonify({"status": "error", "message": str(e)}), 400

        @record_bp.route('/users/me/records', methods=['GET'])
        @jwt_required()
        def get_my_records():
            current_user_id = int(get_jwt_identity())
            user = self.user_repo.get_user_with_records(current_user_id)
            if not user:
                return jsonify({"status": "error", "message": "Пользователь не найден"}), 404
            
            return jsonify([record.to_dict() for record in user.records]), 200

        # --- ОБНОВЛЕНИЕ (ОПТИМИСТИЧНАЯ БЛОКИРОВКА) ---
        @record_bp.route('/records/<int:record_id>', methods=['PUT'])
        @jwt_required()
        def update_record(record_id):
            data = request.get_json()
            try:
                record = self.record_service.update_record_amount(record_id, data['amount'])
                return jsonify(record.to_dict()), 200
            except ValueError as e:
                # Если это ошибка конфликта версий, возвращаем 409
                if "Конфликт" in str(e):
                    return jsonify({"status": "error", "message": str(e)}), 409
                return jsonify({"status": "error", "message": str(e)}), 400