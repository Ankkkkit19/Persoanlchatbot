@echo off
title Ankit's Enhanced Smart Personal Assistant
color 0A
cls

echo.
echo  ==========================================
echo   ANKIT'S ENHANCED SMART PERSONAL ASSISTANT
echo  ==========================================
echo.
echo  Created by: Ankit Kumar Pandit
echo  College: Dev Bhoomi Uttarakhand University
echo  Course: B.Tech CSE (AI/ML)
echo.
echo  ==========================================
echo.
echo  Loading Features:
echo  [*] Schedule Management
echo  [*] Expense Tracking  
echo  [*] Study Assistant
echo  [*] Weather Updates
echo  [*] News and APIs
echo  [*] Motivational Quotes
echo  [*] Programming Jokes
echo  [*] Personal Chatbot
echo.
echo  Starting application in 3 seconds...
echo.

timeout /t 3 /nobreak >nul

REM Clear screen and show starting message
cls
echo.
echo  ==========================================
echo   STARTING CHATBOT...
echo  ==========================================
echo.

REM Check if main file exists
if not exist "simple_enhanced_desktop.py" (
    color 0C
    echo  ERROR: Main application file not found!
    echo.
    echo  Required file: simple_enhanced_desktop.py
    echo  Current folder: %CD%
    echo.
    echo  Please make sure all files are in the same folder.
    echo.
    pause
    exit /b 1
)

REM Try to start the application
echo  Launching GUI application...
echo.

python simple_enhanced_desktop.py

REM Check if application started successfully
if errorlevel 1 (
    color 0E
    echo.
    echo  ==========================================
    echo   TROUBLESHOOTING
    echo  ==========================================
    echo.
    echo  The application could not start. Possible reasons:
    echo.
    echo  1. Python is not installed
    echo     Solution: Download from python.org
    echo.
    echo  2. Python is not in PATH
    echo     Solution: Reinstall Python with "Add to PATH" checked
    echo.
    echo  3. Required packages missing
    echo     Solution: Run "pip install -r requirements.txt"
    echo.
    echo  4. Try alternative Python commands:
    echo.
    
    echo  Trying alternative Python command...
    py simple_enhanced_desktop.py
    
    if errorlevel 1 (
        echo  Trying python3 command...
        python3 simple_enhanced_desktop.py
        
        if errorlevel 1 (
            echo.
            echo  All Python commands failed.
            echo.
            echo  Please:
            echo  1. Install Python from python.org
            echo  2. Make sure to check "Add Python to PATH"
            echo  3. Restart this file
            echo.
            pause
            exit /b 1
        )
    )
)

REM If we reach here, application closed normally
echo.
echo  ==========================================
echo   APPLICATION CLOSED
echo  ==========================================
echo.
echo  Thank you for using Ankit's Smart Assistant!
echo.
pause