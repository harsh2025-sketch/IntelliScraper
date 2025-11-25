@echo off
echo ====================================
echo   IntelliScraper - Quick Start
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install/Update dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create .env file from .env.example and add your API keys.
    echo.
    pause
)

# Start the application
echo Starting IntelliScraper...
echo.
streamlit run main.py

pause
