import pytest
from services import UserService

def test_create_user_success(mocker):
    # Создаем фейковый репозиторий (Mock)
    mock_repo = mocker.Mock()
    mock_repo.create.return_value = {"id": 1, "name": "Alice", "age": 25}
    
    service = UserService(mock_repo)
    result = service.create_user({"name": "Alice", "age": 25})
    
    assert result["name"] == "Alice"
    # Проверяем, что репозиторий был вызван с правильными аргументами
    mock_repo.create.assert_called_once_with("Alice", 25)

def test_create_user_invalid_age(mocker):
    mock_repo = mocker.Mock()
    service = UserService(mock_repo)
    
    # Проверяем, что выбрасывается исключение (ошибочный сценарий)
    with pytest.raises(ValueError, match="Возраст должен быть целым числом от 1 до 120"):
        service.create_user({"name": "Bob", "age": 150})
    
    # Проверяем, что репозиторий НЕ вызывался (так как данные не прошли валидацию)
    mock_repo.create.assert_not_called()

def test_create_user_missing_name(mocker):
    mock_repo = mocker.Mock()
    service = UserService(mock_repo)
    
    with pytest.raises(ValueError, match="Поля 'name' и 'age' обязательны"):
        service.create_user({"age": 20})