from flask import Blueprint, request, jsonify

# Создаем Blueprint для группировки маршрутов
user_bp = Blueprint('users', __name__)

class UserHandler:
    def __init__(self, service):
        self.service = service

    def register_routes(self):
        @user_bp.route('/users', methods=['GET'])
        def get_users():
            users = self.service.get_all_users()
            return jsonify([user.to_dict() for user in users]), 200

        @user_bp.route('/users/<int:user_id>', methods=['GET'])
        def get_user(user_id):
            try:
                user = self.service.get_user(user_id)
                return jsonify(user.to_dict()), 200
            except ValueError as e:
                return jsonify({"status": "error", "code": 404, "message": str(e)}), 404

        @user_bp.route('/users', methods=['POST'])
        def create_user():
            data = request.get_json()
            try:
                user = self.service.create_user(data)
                return jsonify(user.to_dict()), 201
            except ValueError as e:
                return jsonify({"status": "error", "code": 400, "message": str(e)}), 400

        @user_bp.route('/users/<int:user_id>', methods=['PUT'])
        def update_user(user_id):
            data = request.get_json()
            try:
                user = self.service.update_user(user_id, data)
                return jsonify(user.to_dict()), 200
            except ValueError as e:
                # Если ошибка содержит "не найден", возвращаем 404, иначе 400
                status_code = 404 if "не найден" in str(e) else 400
                return jsonify({"status": "error", "code": status_code, "message": str(e)}), status_code

        @user_bp.route('/users/<int:user_id>', methods=['DELETE'])
        def delete_user(user_id):
            try:
                self.service.delete_user(user_id)
                return '', 204
            except ValueError as e:
                return jsonify({"status": "error", "code": 404, "message": str(e)}), 404