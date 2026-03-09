@echo off
echo =========================================
echo   TruthShield AI — Backend Setup
echo =========================================
echo.

cd /d "%~dp0"

echo [1/3] Creating Python virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)
echo     venv created successfully!
echo.

echo [2/3] Activating venv and installing dependencies...
call .venv\Scripts\activate
pip install --upgrade pip --quiet
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo     Dependencies installed!
echo.

echo [3/3] Copying .env.example to .env (if not exists)...
if not exist .env (
    copy .env.example .env
    echo     .env created from template.
) else (
    echo     .env already exists, skipping.
)

echo.
echo =========================================
echo   Setup complete!
echo   To start the server run:
echo     start_server.bat
echo =========================================
pause
