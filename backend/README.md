# Vue3 Chat Backend

FastAPI бэкенд для Vue3 Chat приложения с умным ботом.

## Функциональность

- ✅ REST API для сообщений
- ✅ SQLite база данных
- ✅ Умный чат-бот с контекстными ответами
- ✅ Автоматические ответы бота
- ✅ CORS поддержка
- ✅ Docker контейнеризация

## API Endpoints

### Сообщения
- `GET /messages` - получить все сообщения
- `POST /messages` - отправить новое сообщение
- `DELETE /messages` - очистить все сообщения

### Бот
- `POST /bot/respond` - получить ответ от бота

## Запуск

### Локально
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker-compose up --build
```

## Структура проекта

```
backend/
├── main.py           # FastAPI приложение
├── models.py         # SQLAlchemy модели
├── database.py       # Настройки БД
├── bot.py           # Логика чат-бота
├── requirements.txt  # Зависимости
├── Dockerfile       # Docker образ
└── README.md        # Документация
```

## Особенности бота

- Отвечает на ключевые слова (привет, как дела, спасибо и т.д.)
- Распознает вопросы и эмоции
- Анализирует длину сообщений
- Генерирует контекстные ответы
- Автоматически отвечает через 1-3 секунды 