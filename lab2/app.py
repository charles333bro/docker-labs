from flask import Flask, jsonify, request

app = Flask(__name__)

# Наша "база данных" в оперативной памяти
users = {
    1: {"name": "Alice", "age": 25},
    2: {"name": "Bob", "age": 30}
}
next_id = 3

# 1. GET /users - получить всех пользователей (200 OK)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# 2. GET /users/<id> - получить одного пользователя (200 OK или 404 Not Found)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify(users[user_id]), 200
    return jsonify({"error": "User not found"}), 404

# 3. POST /users - создать нового (201 Created)
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Bad Request. 'name' is required"}), 400
        
    new_user = {"name": data['name'], "age": data.get('age', 0)}
    users[next_id] = new_user
    next_id += 1
    
    return jsonify({"id": next_id - 1, **new_user}), 201

# 4. PUT /users/<id> - обновить пользователя (200 OK или 404 Not Found)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
        
    data = request.get_json()
    if not data:
         return jsonify({"error": "Bad Request"}), 400
         
    users[user_id]['name'] = data.get('name', users[user_id]['name'])
    users[user_id]['age'] = data.get('age', users[user_id]['age'])
    
    return jsonify(users[user_id]), 200

# 5. DELETE /users/<id> - удалить пользователя (204 No Content или 404 Not Found)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204 # 204 означает "Успешно, но контента для возврата нет"
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    # Запускаем на порту 5000, доступным извне контейнера
    app.run(host='0.0.0.0', port=5000, debug=True)