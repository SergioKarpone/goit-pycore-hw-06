@echo off
chcp 65001 >nul
echo ========================================
echo    BOT-ASSISTANT LAUNCHER
echo ========================================
echo.
echo Starting assistant bot...
echo.

python assistant_bot.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Python not found or script failed
    echo ========================================
    echo.
    echo Please check:
    echo 1. Python is installed
    echo 2. Python is in PATH
    echo.
    echo Try running manually:
    echo   python assistant_bot.py
    echo.
    pause
)
