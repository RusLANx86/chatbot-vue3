#!/usr/bin/env python3
"""
Скрипт для инициализации Ollama с моделью
Запускается при первом старте контейнера
"""

import os
import time
import aiohttp
import asyncio
import subprocess
import sys

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
MODEL_NAME = os.getenv('OLLAMA_MODEL', 'llama2:7b')

async def wait_for_ollama():
    """Ждем, пока Ollama станет доступна"""
    print(f"Ожидание запуска Ollama на {OLLAMA_URL}...")
    
    for i in range(30):  # Ждем максимум 30 секунд
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{OLLAMA_URL}/api/tags") as response:
                    if response.status == 200:
                        print("Ollama готова к работе!")
                        return True
        except:
            pass
        
        print(f"Попытка {i+1}/30...")
        await asyncio.sleep(1)
    
    print("Ошибка: Ollama не запустилась за 30 секунд")
    return False

async def check_model():
    """Проверяем, установлена ли модель"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{OLLAMA_URL}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model['name'] for model in data.get('models', [])]
                    return MODEL_NAME in models
    except:
        pass
    return False

async def pull_model():
    """Скачиваем модель"""
    print(f"Скачивание модели {MODEL_NAME}...")
    print("Это может занять несколько минут при первом запуске...")
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "name": MODEL_NAME
            }
            
            async with session.post(f"{OLLAMA_URL}/api/pull", json=payload) as response:
                if response.status == 200:
                    print(f"Модель {MODEL_NAME} успешно скачана!")
                    return True
                else:
                    print(f"Ошибка при скачивании модели: {response.status}")
                    return False
    except Exception as e:
        print(f"Ошибка при скачивании модели: {e}")
        return False

async def test_model():
    """Тестируем модель"""
    print("Тестирование модели...")
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": MODEL_NAME,
                "prompt": "Привет! Как дела?",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 50
                }
            }
            
            async with session.post(f"{OLLAMA_URL}/api/generate", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    response_text = data.get('response', '').strip()
                    print(f"Тест успешен! Ответ модели: {response_text}")
                    return True
                else:
                    print(f"Ошибка при тестировании модели: {response.status}")
                    return False
    except Exception as e:
        print(f"Ошибка при тестировании модели: {e}")
        return False

async def main():
    """Основная функция инициализации"""
    print("=== Инициализация Ollama ===")
    
    # Ждем запуска Ollama
    if not await wait_for_ollama():
        sys.exit(1)
    
    # Проверяем, установлена ли модель
    if await check_model():
        print(f"Модель {MODEL_NAME} уже установлена")
    else:
        # Скачиваем модель
        if not await pull_model():
            print("Не удалось скачать модель. Используем fallback режим.")
            return
    
    # Тестируем модель
    if await test_model():
        print("=== Инициализация завершена успешно! ===")
    else:
        print("=== Инициализация завершена с предупреждениями ===")
        print("Бот будет работать в fallback режиме")

if __name__ == "__main__":
    asyncio.run(main()) 