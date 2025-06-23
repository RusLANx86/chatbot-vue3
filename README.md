# Vue 3 Chat с Ollama LLM

Современный чат-приложение на Vue 3 с FastAPI backend и локальным LLM через Ollama.

## Возможности

- 💬 Чат между пользователями в реальном времени
- 🤖 Умный бот с локальным LLM (Ollama)
- 🔄 WebSocket для мгновенных сообщений
- 📱 Адаптивный дизайн с TailwindCSS
- 🐳 Docker Compose для простого развертывания
- 💾 SQLite база данных для хранения сообщений
- 🌐 CORS поддержка для разработки

## Архитектура

- **Frontend**: Vue 3 + Vite + TailwindCSS + Pinia
- **Backend**: FastAPI + SQLAlchemy + WebSocket
- **LLM**: Ollama с моделью llama2:7b
- **База данных**: SQLite
- **Контейнеризация**: Docker Compose

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Минимум 8GB RAM (для llama2:7b)
- 4GB свободного места на диске

### Запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd vue3_chat
```

2. Запустите все сервисы:
```bash
docker-compose up -d
```

3. Откройте браузер:
```
http://localhost:3000
```

### Первый запуск

При первом запуске:
- Ollama автоматически скачает модель llama2:7b (~4GB)
- Это может занять 10-30 минут в зависимости от интернета
- После скачивания модель работает офлайн

## Конфигурация

### Переменные окружения

В `docker-compose.yml` можно настроить:

```yaml
environment:
  - OLLAMA_URL=http://ollama:11434
  - OLLAMA_MODEL=llama2:7b  # Другие модели: mistral:7b, codellama:7b
  - USE_LLM=true  # false для отключения LLM
```

### Доступные модели Ollama

- `llama2:7b` - базовая модель (4GB)
- `mistral:7b` - быстрая и качественная (4GB)
- `codellama:7b` - для программирования (4GB)
- `llama2:13b` - более качественная (7GB)
- `llama2:70b` - максимальное качество (40GB)

## Разработка

### Локальная разработка

1. Запустите только Ollama:
```bash
docker-compose up ollama -d
```

2. Запустите backend локально:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

3. Запустите frontend локально:
```bash
npm install
npm run dev
```

### Тестирование

#### Запуск всех тестов
```bash
cd backend
pytest -v
```

#### Запуск тестов бота
```bash
cd backend
pytest test_bot.py -v
```

#### Запуск тестов API
```bash
cd backend
pytest test_api.py -v
```

#### Запуск по типам тестов
```bash
# Только unit тесты
pytest -m unit -v

# Только интеграционные тесты
pytest -m integration -v

# Исключить медленные тесты
pytest -m "not slow" -v

# Только быстрые unit тесты
pytest -m "unit and not slow" -v
```

#### Тесты включают:
- ✅ **Unit тесты** (`@pytest.mark.unit`)
  - Инициализация бота
  - Fallback ответы на ключевые слова
  - Fallback ответы на вопросы и эмоции
  - Интеграция с LLM (моки)
  - API endpoints

- ✅ **Интеграционные тесты** (`@pytest.mark.integration`)
  - Полный цикл работы с сообщениями
  - Взаимодействие с ботом
  - Различные типы сообщений

- ✅ **Тесты производительности** (`@pytest.mark.slow`)
  - Множественные ответы
  - Нагрузочное тестирование

- ✅ **API тесты**
  - Все REST endpoints
  - Валидация данных
  - Обработка ошибок

### Структура проекта

```
vue3_chat/
├── src/                    # Vue frontend
│   ├── components/         # Vue компоненты
│   ├── stores/            # Pinia stores
│   └── main.js
├── backend/               # FastAPI backend
│   ├── main.py           # Основной API
│   ├── bot.py            # Логика бота
│   ├── models.py         # SQLAlchemy модели
│   └── database.py       # Настройки БД
├── docker-compose.yml    # Docker конфигурация
└── README.md
```

## API Endpoints

### REST API
- `GET /messages` - получить все сообщения
- `POST /messages` - создать сообщение
- `POST /bot/respond` - получить ответ бота
- `DELETE /messages` - очистить все сообщения

### WebSocket
- `ws://localhost:8000/ws` - реальное время

## Производительность

### Требования к системе

- **Минимум**: 4GB RAM, 2 ядра CPU
- **Рекомендуется**: 8GB RAM, 4 ядра CPU
- **Для больших моделей**: 16GB+ RAM

### Оптимизация

1. Используйте меньшие модели для экономии памяти
2. Настройте `max_tokens` в `bot.py` для контроля длины ответов
3. Используйте `temperature` для контроля креативности

## Устранение неполадок

### Ollama не запускается
```bash
# Проверьте логи
docker-compose logs ollama

# Перезапустите сервис
docker-compose restart ollama
```

### Модель не скачивается
```bash
# Проверьте интернет соединение
# Попробуйте другую модель
# Очистите кэш Docker
docker system prune -a
```

### Медленные ответы
- Уменьшите `max_tokens` в настройках бота
- Используйте более быстрые модели (mistral:7b)
- Увеличьте ресурсы Docker

## Лицензия

MIT License 