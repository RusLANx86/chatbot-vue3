#!/usr/bin/env python3
"""
Скрипт для проверки статуса LLM
"""

import asyncio
import aiohttp
import os
import sys

async def check_llm_status():
    """Проверка статуса LLM"""
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    model_name = os.getenv('OLLAMA_MODEL', 'llama2:7b')
    
    print(f"=== Проверка статуса LLM ===")
    print(f"Ollama URL: {ollama_url}")
    print(f"Модель: {model_name}")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            # Проверяем доступность Ollama
            print("1. Проверка доступности Ollama...")
            async with session.get(f"{ollama_url}/api/tags") as response:
                if response.status == 200:
                    print("✅ Ollama доступна")
                    data = await response.json()
                    models = [model['name'] for model in data.get('models', [])]
                    
                    if model_name in models:
                        print(f"✅ Модель {model_name} найдена")
                        
                        # Тестируем модель
                        print("2. Тестирование модели...")
                        test_payload = {
                            "model": model_name,
                            "prompt": "Привет! Как дела?",
                            "stream": False,
                            "options": {
                                "temperature": 0.7,
                                "max_tokens": 50
                            }
                        }
                        
                        async with session.post(
                            f"{ollama_url}/api/generate",
                            json=test_payload,
                            timeout=aiohttp.ClientTimeout(total=10)
                        ) as test_response:
                            if test_response.status == 200:
                                test_data = await test_response.json()
                                response_text = test_data.get('response', '').strip()
                                print("✅ Модель работает!")
                                print(f"   Тестовый ответ: {response_text}")
                                return True
                            else:
                                print(f"❌ Ошибка тестирования модели: {test_response.status}")
                                return False
                    else:
                        print(f"❌ Модель {model_name} не найдена")
                        print(f"   Доступные модели: {', '.join(models) if models else 'нет'}")
                        return False
                else:
                    print(f"❌ Ollama недоступна: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

async def main():
    """Основная функция"""
    success = await check_llm_status()
    
    print()
    if success:
        print("🎉 LLM готов к работе!")
        sys.exit(0)
    else:
        print("💥 LLM не готов к работе")
        print("\nВозможные решения:")
        print("1. Убедитесь, что Ollama запущена")
        print("2. Скачайте модель: ollama pull llama2:7b")
        print("3. Проверьте переменные окружения OLLAMA_URL и OLLAMA_MODEL")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 