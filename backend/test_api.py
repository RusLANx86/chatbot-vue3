import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

@pytest.fixture
def test_client():
    """Фикстура для тестового клиента"""
    return client

@pytest.mark.unit
class TestAPIEndpoints:
    """Unit тесты для API endpoints"""
    
    def test_root_endpoint(self, test_client):
        """Тест корневого endpoint"""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Vue3 Chat API"
        assert "version" in data
    
    def test_get_messages_empty(self, test_client):
        """Тест получения пустого списка сообщений"""
        response = test_client.get("/messages")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_message(self, test_client):
        """Тест создания сообщения"""
        message_data = {
            "sender": "User A",
            "text": "Тестовое сообщение"
        }
        
        response = test_client.post("/messages", json=message_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["sender"] == "User A"
        assert data["text"] == "Тестовое сообщение"
        assert "id" in data
        assert "timestamp" in data
    
    def test_create_message_invalid_data(self, test_client):
        """Тест создания сообщения с неверными данными"""
        # Отсутствует текст
        message_data = {"sender": "User A"}
        response = test_client.post("/messages", json=message_data)
        assert response.status_code == 422
        
        # Отсутствует отправитель
        message_data = {"text": "Тестовое сообщение"}
        response = test_client.post("/messages", json=message_data)
        assert response.status_code == 422
    
    @patch('main.chat_bot.get_response')
    def test_bot_respond_endpoint(self, mock_get_response, test_client):
        """Тест endpoint для ответа бота"""
        mock_get_response.return_value = "Тестовый ответ бота"
        
        message_data = {
            "sender": "User A",
            "text": "Привет"
        }
        
        response = test_client.post("/bot/respond", json=message_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["sender"] == "Bot"
        assert data["text"] == "Тестовый ответ бота"
        assert "id" in data
        assert "timestamp" in data
    
    def test_clear_messages(self, test_client):
        """Тест очистки сообщений"""
        # Сначала создаем сообщение
        message_data = {"sender": "User A", "text": "Тест"}
        test_client.post("/messages", json=message_data)
        
        # Очищаем сообщения
        response = test_client.delete("/messages")
        assert response.status_code == 200
        
        # Проверяем, что сообщения очищены
        response = test_client.get("/messages")
        assert response.json() == []

@pytest.mark.integration
class TestAPIIntegration:
    """Интеграционные тесты для API"""
    
    def test_full_message_flow(self, test_client):
        """Тест полного цикла работы с сообщениями"""
        # 1. Создаем сообщение
        message_data = {"sender": "User A", "text": "Интеграционный тест"}
        response = test_client.post("/messages", json=message_data)
        assert response.status_code == 200
        
        # 2. Получаем список сообщений
        response = test_client.get("/messages")
        assert response.status_code == 200
        messages = response.json()
        assert len(messages) >= 1
        
        # 3. Проверяем, что наше сообщение есть в списке
        user_message = next((m for m in messages if m["text"] == "Интеграционный тест"), None)
        assert user_message is not None
        assert user_message["sender"] == "User A"
    
    @patch('main.chat_bot.get_response')
    def test_bot_interaction_flow(self, mock_get_response, test_client):
        """Тест цикла взаимодействия с ботом"""
        mock_get_response.return_value = "Привет! Рад тебя видеть!"
        
        # 1. Отправляем сообщение пользователя
        user_message = {"sender": "User A", "text": "Привет"}
        response = test_client.post("/messages", json=user_message)
        assert response.status_code == 200
        
        # 2. Получаем ответ бота
        bot_response = test_client.post("/bot/respond", json=user_message)
        assert bot_response.status_code == 200
        
        bot_data = bot_response.json()
        assert bot_data["sender"] == "Bot"
        assert "Привет" in bot_data["text"]

@pytest.mark.asyncio
class TestAsyncEndpoints:
    """Тесты асинхронных endpoints"""
    
    @pytest.mark.asyncio
    async def test_bot_status_endpoint(self, test_client):
        """Тест endpoint статуса бота"""
        with patch('aiohttp.ClientSession') as mock_session:
            # Мокаем успешный ответ от Ollama
            mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value.status = 200
            mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value.json = AsyncMock(return_value={
                "models": [{"name": "llama2:7b"}]
            })
            
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.status = 200
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.json = AsyncMock(return_value={
                "response": "test"
            })
            
            response = test_client.get("/bot/status")
            assert response.status_code == 200
            
            data = response.json()
            assert "status" in data
            assert data["status"] in ["ready", "loading", "error"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 