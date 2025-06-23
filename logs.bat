@echo off
echo ========================================
echo    Логи Vue 3 Chat
echo ========================================
echo.

echo Выберите сервис для просмотра логов:
echo 1. Все сервисы
echo 2. Frontend
echo 3. Backend
echo 4. Ollama
echo 5. Выход
echo.

set /p choice="Введите номер (1-5): "

if "%choice%"=="1" (
    echo Показ логов всех сервисов...
    docker-compose logs -f
) else if "%choice%"=="2" (
    echo Показ логов Frontend...
    docker-compose logs -f frontend
) else if "%choice%"=="3" (
    echo Показ логов Backend...
    docker-compose logs -f backend
) else if "%choice%"=="4" (
    echo Показ логов Ollama...
    docker-compose logs -f ollama
) else if "%choice%"=="5" (
    echo Выход...
    exit /b
) else (
    echo Неверный выбор!
    pause
    exit /b
)

echo.
pause 