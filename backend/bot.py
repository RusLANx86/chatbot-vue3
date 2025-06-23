import random
import re
import os
import aiohttp
import asyncio
from typing import Optional

class ChatBot:
    def __init__(self):
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.model_name = os.getenv('OLLAMA_MODEL', 'llama2:7b')
        self.use_llm = os.getenv('USE_LLM', 'true').lower() == 'true'
        
        # Fallback ответы для случаев, когда LLM недоступен
        self.responses = {
            "привет": [
                "Привет! Как дела?",
                "Привет! Рад тебя видеть!",
                "Привет! Чем могу помочь?",
                "Привет! Как настроение?"
            ],
            "как дела": [
                "Отлично! Спасибо, что спросил!",
                "Хорошо! А у тебя как?",
                "Все супер! Готов к общению!",
                "Замечательно! Надеюсь, у тебя тоже все хорошо!"
            ],
            "что делаешь": [
                "Общаюсь с тобой! 😊",
                "Изучаю новые сообщения",
                "Помогаю людям в чате",
                "Отвечаю на интересные вопросы"
            ],
            "спасибо": [
                "Пожалуйста! Рад помочь!",
                "Не за что! Обращайся!",
                "Спасибо тебе за общение!",
                "Всегда рад быть полезным!"
            ],
            "пока": [
                "До свидания! Было приятно пообщаться!",
                "Пока! Надеюсь, скоро увидимся!",
                "До встречи! Хорошего дня!",
                "Пока! Не скучай!"
            ]
        }
        
        self.general_responses = [
            "Интересно! Расскажи подробнее.",
            "Понятно, что ты имеешь в виду.",
            "Это очень интересная мысль!",
            "Согласен с тобой.",
            "Хм, нужно подумать об этом.",
            "Отличная идея!",
            "Спасибо за информацию.",
            "Это заставляет задуматься.",
            "Очень хорошо сказано!",
            "Продолжай, мне интересно.",
            "Ух ты! Это действительно интересно!",
            "Я тоже так думаю!",
            "Хороший вопрос!",
            "Давайте обсудим это подробнее.",
            "Я внимательно слушаю!"
        ]
        
        self.questions = [
            "А что ты думаешь об этом?",
            "Как ты к этому относишься?",
            "Расскажи больше!",
            "Это правда интересно!",
            "А что дальше?",
            "Как это работает?",
            "Почему ты так думаешь?",
            "Что тебя вдохновляет?"
        ]

    async def get_llm_response(self, message: str) -> Optional[str]:
        """Получить ответ от Ollama LLM"""
        if not self.use_llm:
            return None
            
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": f"""Ты дружелюбный чат-бот. Отвечай кратко и по-русски на сообщение пользователя.

Сообщение пользователя: {message}

Ответ:""",
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 150
                    }
                }
                
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', '').strip()
                    else:
                        print(f"Ollama API error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return None

    def get_fallback_response(self, message: str) -> str:
        """Получить fallback ответ"""
        message_lower = message.lower().strip()
        
        for keyword, responses in self.responses.items():
            if keyword in message_lower:
                return random.choice(responses)
        
        if message_lower.endswith('?') or message_lower.startswith('что') or message_lower.startswith('как') or message_lower.startswith('почему'):
            return random.choice(self.questions)
        
        if len(message_lower) < 10:
            return random.choice(self.general_responses)
        
        if any(emoji in message_lower for emoji in ['😊', '😄', '😍', '😎', '👍', '❤️']):
            return "Отличное настроение! 😊"
        
        if any(emoji in message_lower for emoji in ['😢', '😭', '😔', '😞', '💔']):
            return "Не грусти! Все будет хорошо! 🌟"
        
        if re.search(r'\d+', message_lower):
            return "Цифры! Интересно! Расскажи больше об этом."
        
        if len(message_lower) > 50:
            return "Вау! Ты очень подробно все объяснил! Спасибо за информацию!"
        
        return random.choice(self.general_responses)

    async def get_response(self, message: str) -> str:
        """Получить ответ бота (LLM или fallback)"""
        llm_response = await self.get_llm_response(message)
        
        if llm_response and len(llm_response) > 0:
            return llm_response
        else:
            return self.get_fallback_response(message)

    def get_response_sync(self, message: str) -> str:
        """Синхронная версия для совместимости"""
        return asyncio.run(self.get_response(message))