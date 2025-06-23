@echo off
echo ========================================
echo    Остановка Vue 3 Chat
echo ========================================
echo.

echo Остановка Docker Compose...
docker-compose down

echo.
echo Очистка неиспользуемых ресурсов...
docker system prune -f

echo.
echo ========================================
echo Все сервисы остановлены!
echo ========================================
echo.
pause 