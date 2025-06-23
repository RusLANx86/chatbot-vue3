import pytest
import asyncio
import aiohttp
import os
from unittest.mock import patch, AsyncMock
from bot import ChatBot

@pytest.fixture
def chat_bot():
    """Фикстура для создания экземпляра бота"""
    return ChatBot()

@pytest.fixture
def mock_ollama_response():
    """Мок ответа от Ollama"""
    return {
        "response": "Привет! Как дела? Рад тебя видеть!",
        "done": True
    }

@pytest.mark.unit
class TestChatBot:
    """Unit тесты для ChatBot"""
    
    def test_bot_initialization(self, chat_bot):
        """Тест инициализации бота"""
        assert chat_bot.ollama_url == os.getenv('OLLAMA_URL', 'http://localhost:11434')
        assert chat_bot.model_name == os.getenv('OLLAMA_MODEL', 'llama2:7b')
        assert chat_bot.use_llm == (os.getenv('USE_LLM', 'true').lower() == 'true')
    
    @pytest.mark.parametrize("input_text,expected_keywords", [
        ("Привет!", ["привет", "рад", "видеть"]),
        ("Как дела?", ["хорошо", "отлично", "спасибо"]),
        ("Спасибо!", ["пожалуйста", "рад", "помочь"]),
        ("Пока!", ["до свидания", "встречи", "дня"]),
    ])
    def test_fallback_response_keywords(self, chat_bot, input_text, expected_keywords):
        """Тест fallback ответов на ключевые слова"""
        response = chat_bot.get_fallback_response(input_text)
        assert any(word in response.lower() for word in expected_keywords)
    
    @pytest.mark.parametrize("input_text", [
        "Что ты думаешь?",
        "Как это работает?",
        "Почему так происходит?",
    ])
    def test_fallback_response_questions(self, chat_bot, input_text):
        """Тест fallback ответов на вопросы"""
        response = chat_bot.get_fallback_response(input_text)
        assert "?" in response or "расскажи" in response.lower()
    
    @pytest.mark.parametrize("input_text,expected_emotion", [
        ("Я рад! 😊", ["настроение", "отлично"]),
        ("Мне грустно 😢", ["грусти", "хорошо"]),
        ("Я счастлив! 😍", ["настроение", "отлично"]),
    ])
    def test_fallback_response_emotions(self, chat_bot, input_text, expected_emotion):
        """Тест fallback ответов на эмоции"""
        response = chat_bot.get_fallback_response(input_text)
        assert any(word in response.lower() for word in expected_emotion)
    
    @pytest.mark.asyncio
    async def test_llm_response_success(self, chat_bot, mock_ollama_response):
        """Тест успешного ответа от LLM"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.status = 200
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_ollama_response)
            
            response = await chat_bot.get_llm_response("Привет!")
            assert response == "Привет! Как дела? Рад тебя видеть!"
    
    @pytest.mark.asyncio
    async def test_llm_response_error(self, chat_bot):
        """Тест ошибки при обращении к LLM"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.status = 404
            
            response = await chat_bot.get_llm_response("Привет!")
            assert response is None
    
    @pytest.mark.asyncio
    async def test_llm_disabled(self, chat_bot):
        """Тест отключенного LLM"""
        chat_bot.use_llm = False
        response = await chat_bot.get_llm_response("Привет!")
        assert response is None
    
    @pytest.mark.asyncio
    async def test_get_response_with_llm(self, chat_bot, mock_ollama_response):
        """Тест получения ответа с LLM"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.status = 200
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_ollama_response)
            
            response = await chat_bot.get_response("Привет!")
            assert "Привет! Как дела? Рад тебя видеть!" in response
    
    @pytest.mark.asyncio
    async def test_get_response_fallback(self, chat_bot):
        """Тест получения fallback ответа"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value.status = 404
            
            response = await chat_bot.get_response("Привет!")
            assert any(word in response.lower() for word in ["привет", "рад", "видеть"])

@pytest.mark.integration
class TestBotIntegration:
    """Интеграционные тесты"""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_text", [
        "Привет",
        "Что ты умеешь?",
        "Это очень длинное сообщение с множеством слов и деталей, которые должны вызвать определенную реакцию у бота",
        "Мне 25 лет",
    ])
    async def test_bot_response_types(self, chat_bot, input_text):
        """Тест различных типов ответов бота"""
        response = await chat_bot.get_response(input_text)
        assert len(response) > 0
        assert isinstance(response, str)

@pytest.mark.slow
class TestBotPerformance:
    """Тесты производительности (медленные)"""
    
    @pytest.mark.asyncio
    async def test_multiple_responses(self, chat_bot):
        """Тест множественных ответов"""
        responses = []
        for i in range(5):
            response = await chat_bot.get_response(f"Сообщение {i}")
            responses.append(response)
        
        assert len(responses) == 5
        assert all(len(r) > 0 for r in responses)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 