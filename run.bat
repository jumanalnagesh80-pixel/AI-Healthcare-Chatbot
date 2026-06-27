@echo off
REM AI Healthcare Chatbot - Quick Start Script for Windows

echo ========================================
echo AI Healthcare Chatbot - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python is installed
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed
echo.

REM Setup database
echo Setting up database with sample data...
python setup.py

if %errorlevel% neq 0 (
    echo Error: Failed to setup database
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting the application...
echo Access at: http://localhost:5000
echo Press Ctrl+C to stop
echo ========================================
echo.

python app.py

pause
