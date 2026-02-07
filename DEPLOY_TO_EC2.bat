@echo off
title Deploy to AWS EC2
echo.
echo ========================================
echo   DEPLOY TO AWS EC2
echo   Smart Personal Assistant
echo ========================================
echo.

REM Configuration - UPDATE THESE VALUES
set EC2_IP=YOUR_EC2_PUBLIC_IP
set KEY_FILE=path\to\your-key.pem
set EC2_USER=ubuntu

echo Please update EC2_IP and KEY_FILE in this script before running!
echo.
echo Current settings:
echo   EC2 IP: %EC2_IP%
echo   Key File: %KEY_FILE%
echo.
pause

echo.
echo Step 1: Uploading files to EC2...
echo.

REM Upload Python files
scp -i "%KEY_FILE%" app_web.py %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" chatbot.py %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" dataset_bot.py %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" dataset_trainer.py %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" intent_to_dataset.py %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" web_search_helper.py %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" multi_api_assistant.py %EC2_USER%@%EC2_IP%:~/chatbot/

REM Upload data files
scp -i "%KEY_FILE%" dataset.json %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" intents.json %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" assistant_data.json %EC2_USER%@%EC2_IP%:~/chatbot/

REM Upload directories
scp -i "%KEY_FILE%" -r static %EC2_USER%@%EC2_IP%:~/chatbot/
scp -i "%KEY_FILE%" -r templates %EC2_USER%@%EC2_IP%:~/chatbot/

echo.
echo Step 2: Restarting service on EC2...
ssh -i "%KEY_FILE%" %EC2_USER%@%EC2_IP% "sudo systemctl restart chatbot"

echo.
echo ========================================
echo   DEPLOYMENT COMPLETED!
echo ========================================
echo.
echo Your chatbot is now live at:
echo   http://%EC2_IP%
echo.
echo To view logs:
echo   ssh -i "%KEY_FILE%" %EC2_USER%@%EC2_IP%
echo   sudo journalctl -u chatbot -f
echo.
pause