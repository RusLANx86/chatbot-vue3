FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Делаем скрипт инициализации исполняемым
RUN chmod +x init_ollama.py

# Создаем директорию для данных
RUN mkdir -p data

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Открываем порт
EXPOSE 8000

# Запускаем инициализацию Ollama и затем приложение
CMD ["sh", "-c", "python init_ollama.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"] 