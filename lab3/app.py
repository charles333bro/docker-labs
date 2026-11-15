from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

# Настройка логирования (вывод ошибок в консоль Docker)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# "База данных"
users = {
    1: {"name": "Alice", "age": 25},
    2: {"name": "Bob", "age": 30}
}
next_id = 3

# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ВАЛИДАЦИИ ---
def validate_user_data(data, is_update=False):
    errors = []
    
    # Валидация имени (если это создание, имя обязательно)
    if not is_update or 'name' in data:
        name = data.get('name')
        if not name:
            errors.append("Поле 'name' обязательно")
        elif not isinstance(name, str):
            errors.append("Поле 'name' должно быть строкой")
        elif len(name) < 3:
            errors.append("Имя должно содержать минимум 3 символа (бизнес-правило)")
            
    # Валидация возраста
    if not is_update or 'age' in data:
        age = data.get('age')
        if age is None:
            errors.append("Поле 'age' обязательно")
        elif not isinstance(age, int):
            errors.append("Поле 'age' должно быть целым числом")
        elif age < 1 or age > 120:
            errors.append("Возраст должен быть от 1 до 120 лет (диапазон)")
            
    return errors

# --- ЭНДПОИНТЫ С ОБРАБОТКОЙ ОШИБОК ---

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        # Структурированная ошибка 404
        return jsonify({"status": "error", "code": 404, "message": f"Пользователь с ID {user_id} не найден"}), 404
    return jsonify(users[user_id]), 200

@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "code": 400, "message": "Тело запроса не может быть пустым. Ожидается JSON."}), 400

    # Валидация
    errors = validate_user_data(data)
    if errors:
        # Логируем ошибку валидации
        logger.warning(f"Ошибка валидации при создании: {errors}")
        # Возвращаем структурированную ошибку 400
        return jsonify({
            "status": "error", 
            "code": 400, 
            "message": "Ошибка валидации входных данных", 
            "details": errors
        }), 400

    new_user = {"name": data['name'], "age": data['age']}
    users[next_id] = new_user
    next_id += 1
    
    return jsonify({"id": next_id - 1, **new_user}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"status": "error", "code": 404, "message": f"Пользователь с ID {user_id} не найден"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "code": 400, "message": "Тело запроса не может быть пустым."}), 400

    # Валидация (is_update=True позволяет обновлять только одно поле)
    errors = validate_user_data(data, is_update=True)
    if errors:
        logger.warning(f"Ошибка валидации при обновлении ID {user_id}: {errors}")
        return jsonify({
            "status": "error", 
            "code": 400, 
            "message": "Ошибка валидации входных данных", 
            "details": errors
        }), 400

    users[user_id]['name'] = data.get('name', users[user_id]['name'])
    users[user_id]['age'] = data.get('age', users[user_id]['age'])
    
    return jsonify(users[user_id]), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204
    return jsonify({"status": "error", "code": 404, "message": f"Пользователь с ID {user_id} не найден"}), 404

# --- ГЛОБАЛЬНЫЙ ОБРАБОТЧИК 500 (Внутренние ошибки сервера) ---
@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Критическая ошибка сервера (500): {error}")
    return jsonify({
        "status": "error",
        "code": 500,
        "message": "Внутренняя ошибка сервера. Мы уже работаем над этим."
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)