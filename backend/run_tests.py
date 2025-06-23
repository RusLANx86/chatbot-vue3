#!/usr/bin/env python3
"""
Скрипт для запуска тестов бота
"""

import sys
import os

def run_tests():
    """Запуск тестов"""
    print("=== Запуск тестов Vue 3 Chat ===")
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists('test_bot.py'):
        print("Ошибка: test_bot.py не найден в текущей директории")
        sys.exit(1)
    
    # Импортируем и запускаем pytest напрямую
    try:
        import pytest
        sys.exit(pytest.main([
            'test_bot.py', 
            '-v', 
            '--tb=short',
            '--color=yes'
        ]))
    except ImportError:
        print("Ошибка: pytest не установлен. Установите: pip install pytest pytest-asyncio")
        sys.exit(1)

if __name__ == "__main__":
    run_tests() 