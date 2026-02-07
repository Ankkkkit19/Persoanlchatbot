@echo off
title Installing Voice & Face Recognition Dependencies
color 0A

echo.
echo  ==========================================
echo   INSTALLING VOICE & FACE RECOGNITION
echo  ==========================================
echo.
echo  This will install required packages for:
echo  - Voice Recognition (Speech-to-Text)
echo  - Text-to-Speech
echo  - Face Recognition
echo  - Camera Integration
echo.
echo  Please wait, this may take 5-10 minutes...
echo.

REM Install basic requirements first
echo [1/6] Installing basic requirements...
pip install numpy pillow requests scikit-learn

REM Install voice recognition
echo [2/6] Installing speech recognition...
pip install SpeechRecognition pyttsx3

REM Install audio support
echo [3/6] Installing audio support...
pip install pyaudio

REM Install OpenCV for camera
echo [4/6] Installing OpenCV for camera...
pip install opencv-python

REM Install face recognition (this takes longest)
echo [5/6] Installing face recognition (this may take a while)...
pip install face-recognition

REM Install dlib (face recognition dependency)
echo [6/6] Installing dlib...
pip install dlib

echo.
echo  ==========================================
echo   INSTALLATION COMPLETE!
echo  ==========================================
echo.
echo  You can now run:
echo  python voice_face_assistant.py
echo.
echo  Features available:
echo  - Voice commands
echo  - Face recognition
echo  - Text-to-speech
echo  - Camera integration
echo.
pause