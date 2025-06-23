@echo off
echo ========================================
echo    Vue 3 Chat с Ollama LLM
echo ========================================
echo.

echo Запуск Docker Compose...
docker-compose up -d

echo.
echo Ожидание запуска сервисов...
timeout /t 10 /nobreak > nul

echo.
echo Проверка статуса сервисов...
docker-compose ps

echo.
echo ========================================
echo Сервисы запущены!
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Ollama: http://localhost:11434
echo.
echo При первом запуске Ollama скачает модель
echo llama2:7b (~4GB). Это может занять 10-30 минут.
echo ========================================
echo.
pause 