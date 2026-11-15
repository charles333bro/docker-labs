def test_create_user_api(client):
    # Отправляем POST запрос
    response = client.post('/users', json={"name": "IntegrationTest", "age": 20})
    
    # Проверяем статус-код и данные в ответе
    assert response.status_code == 201
    assert response.json["name"] == "IntegrationTest"
    assert response.json["age"] == 20

def test_get_users_api(client):
    # Сначала создадим пользователя, чтобы список не был пустым
    client.post('/users', json={"name": "GetTest", "age": 30})
    
    # Отправляем GET запрос
    response = client.get('/users')
    
    assert response.status_code == 200
    assert len(response.json) > 0
    assert isinstance(response.json, list)

def test_get_user_not_found_api(client):
    # Запрашиваем несуществующего пользователя (граничный/ошибочный сценарий)
    response = client.get('/users/9999')
    
    assert response.status_code == 404
    assert response.json["status"] == "error"