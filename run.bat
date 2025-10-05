@echo off
REM CTA Evaluation System - Quick Launch Script
REM This script activates the virtual environment and runs the application

REM Set console to UTF-8 encoding for proper character display
chcp 65001 > nul

echo ============================================
echo CTA Evaluation System
echo ============================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting application...
python main.py

pause

