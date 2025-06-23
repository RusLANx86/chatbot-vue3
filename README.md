# Vue 3 Chat Application

Полнофункциональное Vue 3 приложение для чата с FastAPI бэкендом и умным ботом.

## Функциональность

### Frontend (Vue 3)
- ✅ Форма отправки сообщения с валидацией
- ✅ Выбор пользователя (User A / User B)
- ✅ Список сообщений в хронологическом порядке
- ✅ Визуальное различие сообщений от разных пользователей
- ✅ **Умный чат-бот с автоматическими ответами**
- ✅ **REST API интеграция**
- ✅ Сохранение сообщений в базе данных
- ✅ Статистика сообщений и ответов бота

### Backend (FastAPI)
- ✅ REST API для сообщений
- ✅ SQLite база данных
- ✅ Умный чат-бот с контекстными ответами
- ✅ Docker контейнеризация
- ✅ CORS поддержка

## Архитектура

### Frontend (Vue 3)
- **Vue 3** с Composition API
- **Pinia** для управления состоянием
- **Vite** для сборки
- **TailwindCSS** для стилизации
- **Fetch API** для работы с REST API

### Backend (FastAPI)
- **FastAPI** для REST API
- **SQLAlchemy** для работы с БД
- **SQLite** база данных
- **Python 3.11** с Docker

## Установка и запуск

### 1. Запуск бэкенда

#### Вариант A: Docker (рекомендуется)
```bash
docker-compose up --build
```

#### Вариант B: Локально
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Бэкенд будет доступен на `http://localhost:8000`

### 2. Запуск фронтенда

```bash
npm install
npm run dev
```

Фронтенд будет доступен на `http://localhost:3000`

### 3. API документация

После запуска бэкенда доступна автоматическая документация:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Сообщения
- `GET /messages` - получить все сообщения
- `POST /messages` - отправить новое сообщение
- `DELETE /messages` - очистить все сообщения

### Бот
- `POST /bot/respond` - получить ответ от бота

## Особенности бота

🤖 **Умный чат-бот** автоматически отвечает на сообщения:

- **Ключевые слова**: привет, как дела, спасибо, пока
- **Вопросы**: распознает вопросительные предложения
- **Эмоции**: реагирует на эмодзи и эмоциональные сообщения
- **Контекст**: анализирует длину и содержание сообщений
- **Автоматические ответы**: отвечает через 1-3 секунды

## Структура проекта

```
vue3_chat/
├── src/                    # Frontend (Vue 3)
│   ├── components/
│   │   ├── ChatHeader.vue      # Заголовок с статистикой
│   │   ├── UserSelector.vue    # Выбор пользователя
│   │   ├── MessageList.vue     # Список сообщений
│   │   └── MessageForm.vue     # Форма отправки
│   ├── stores/
│   │   └── chat.js            # Pinia store с REST API
│   ├── App.vue                # Главный компонент
│   ├── main.js                # Точка входа
│   └── style.css              # Глобальные стили
├── backend/                  # Backend (FastAPI)
│   ├── main.py               # FastAPI приложение
│   ├── models.py             # SQLAlchemy модели
│   ├── database.py           # Настройки БД
│   ├── bot.py               # Логика чат-бота
│   ├── requirements.txt      # Зависимости
│   ├── Dockerfile           # Docker образ
│   └── README.md            # Документация
├── package.json             # Зависимости фронтенда
├── vite.config.js           # Конфигурация Vite
├── tailwind.config.js       # Конфигурация TailwindCSS
├── docker-compose.yml       # Docker Compose
└── README.md                # Основная документация
```

## Технологии

### Frontend
- **Vue 3** (Composition API)
- **Pinia** (стейт-менеджер)
- **Vite** (сборка)
- **TailwindCSS** (стили)

### Backend
- **FastAPI** (веб-фреймворк)
- **SQLAlchemy** (ORM)
- **SQLite** (база данных)
- **Python 3.11** (язык программирования)

### DevOps
- **Docker** (контейнеризация)
- **Docker Compose** (оркестрация) 