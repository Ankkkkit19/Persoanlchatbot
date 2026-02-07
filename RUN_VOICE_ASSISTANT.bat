@echo off
title Voice Assistant Chatbot
color 0B

echo.
echo  ==========================================
echo   VOICE ASSISTANT CHATBOT
echo  ==========================================
echo.
echo  Created by: Ankit Kumar Pandit
echo  Features: Voice Commands + Text-to-Speech
echo.
echo  ==========================================
echo.
echo  Loading Voice Features:
echo  [*] Voice Recognition (Speech-to-Text)
echo  [*] Text-to-Speech Response
echo  [*] Natural Voice Conversation
echo  [*] All Previous Chatbot Features
echo.
echo  Starting application...
echo.

timeout /t 3 /nobreak >nul

REM Check if main file exists
if not exist "voice_assistant_simple.py" (
    color 0C
    echo  ERROR: voice_assistant_simple.py not found!
    echo.
    echo  Please make sure the file is in the same folder.
    echo.
    pause
    exit /b 1
)

REM Try to start the application
echo  Launching Voice Assistant Chatbot...
echo.

python voice_assistant_simple.py

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
    echo     Solution: pip install SpeechRecognition pyttsx3
    echo.
    echo  2. Microphone not available
    echo     Solution: Connect microphone or enable built-in mic
    echo.
    echo  3. Audio drivers missing
    echo     Solution: Update audio drivers
    echo.
    pause
    exit /b 1
)

echo.
echo  ==========================================
echo   APPLICATION CLOSED
echo  ==========================================
echo.
echo  Thank you for using Voice Assistant Chatbot!
echo.
pause