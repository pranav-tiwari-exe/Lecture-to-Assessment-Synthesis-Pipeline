@echo off
REM Start all services for development on Windows

echo Starting RPKP Development Environment...
echo.

REM Start Backend
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && npm start"

timeout /t 3 /nobreak >nul

REM Start ML Service
echo Starting ML Service...
start "ML Service" cmd /k "cd ml && venv\Scripts\activate && uvicorn server:app --reload --port 8000"

timeout /t 3 /nobreak >nul

REM Start Frontend
echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo All services started!
echo.
echo Services:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:5000
echo   ML Service: http://localhost:8000
echo.
echo Close the windows to stop services
pause
