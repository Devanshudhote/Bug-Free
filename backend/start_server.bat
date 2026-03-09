@echo off
echo =========================================
echo   TruthShield AI — Starting Server
echo =========================================
echo.
cd /d "%~dp0"
call .venv\Scripts\activate
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
