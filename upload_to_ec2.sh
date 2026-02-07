#!/bin/bash
# Script to upload files from Windows to EC2
# Run this from Git Bash or WSL on Windows

# Configuration
EC2_IP="YOUR_EC2_PUBLIC_IP"
KEY_FILE="path/to/your-key.pem"
LOCAL_DIR="."
REMOTE_DIR="/home/ubuntu/chatbot"

echo "🚀 Uploading files to EC2..."
echo "============================================================"

# Check if key file exists
if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Error: Key file not found: $KEY_FILE"
    echo "Please update KEY_FILE variable in this script"
    exit 1
fi

# Set correct permissions for key file
chmod 400 "$KEY_FILE"

# Files to upload
FILES=(
    "app_web.py"
    "enhanced_web_app.py"
    "chatbot.py"
    "dataset_bot.py"
    "dataset_trainer.py"
    "intent_to_dataset.py"
    "web_search_helper.py"
    "multi_api_assistant.py"
    "dataset.json"
    "intents.json"
    "assistant_data.json"
    "requirements.txt"
)

# Directories to upload
DIRS=(
    "static"
    "templates"
)

echo "📦 Uploading Python files..."
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  Uploading $file..."
        scp -i "$KEY_FILE" "$file" ubuntu@$EC2_IP:$REMOTE_DIR/
    else
        echo "  ⚠️  Skipping $file (not found)"
    fi
done

echo ""
echo "📁 Uploading directories..."
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  Uploading $dir/..."
        scp -i "$KEY_FILE" -r "$dir" ubuntu@$EC2_IP:$REMOTE_DIR/
    else
        echo "  ⚠️  Skipping $dir/ (not found)"
    fi
done

echo ""
echo "🔄 Restarting chatbot service on EC2..."
ssh -i "$KEY_FILE" ubuntu@$EC2_IP "sudo systemctl restart chatbot"

echo ""
echo "============================================================"
echo "✅ Upload completed!"
echo "🌐 Access your chatbot at: http://$EC2_IP"
echo ""
echo "📝 To view logs:"
echo "   ssh -i \"$KEY_FILE\" ubuntu@$EC2_IP"
echo "   sudo journalctl -u chatbot -f"
echo "============================================================"