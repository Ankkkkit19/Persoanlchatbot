@echo off
title Voice & Face Recognition Assistant
color 0B

echo.
echo  ==========================================
echo   VOICE & FACE RECOGNITION ASSISTANT
echo  ==========================================
echo.
echo  Created by: Ankit Kumar Pandit
echo  Features: Voice Commands + Face Recognition
echo.
echo  ==========================================
echo.
echo  Loading Advanced Features:
echo  [*] Voice Recognition (Speech-to-Text)
echo  [*] Text-to-Speech Response
echo  [*] Face Recognition & Authentication
echo  [*] Camera Integration
echo  [*] All Previous Chatbot Features
echo.
echo  Starting application...
echo.

timeout /t 3 /nobreak >nul

REM Check if main file exists
if not exist "voice_face_assistant.py" (
    color 0C
    echo  ERROR: voice_face_assistant.py not found!
    echo.
    echo  Please make sure the file is in the same folder.
    echo.
    pause
    exit /b 1
)

REM Try to start the application
echo  Launching Voice & Face Recognition Assistant...
echo.

python voice_face_assistant.py

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
    echo  1. Required packages not installed
    echo     Solution: Run "install_voice_face.bat" first
    echo.
    echo  2. Camera not available
    echo     Solution: Connect a webcam or enable built-in camera
    echo.
    echo  3. Microphone not available
    echo     Solution: Connect microphone or enable built-in mic
    echo.
    echo  4. Python packages missing
    echo     Solution: pip install -r requirements_voice_face.txt
    echo.
    pause
    exit /b 1
)

echo.
echo  ==========================================
echo   APPLICATION CLOSED
echo  ==========================================
echo.
echo  Thank you for using Voice & Face Recognition Assistant!
echo.
pause