#!/bin/bash
# Automated EC2 Deployment Script for Ubuntu
# Run this script on your EC2 instance after connecting via SSH

set -e  # Exit on error

echo "🚀 Starting Smart Personal Assistant Deployment on EC2..."
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Step 1: Update system
print_status "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 2: Install dependencies
print_status "Step 2: Installing dependencies..."
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor

# Step 3: Create application directory
print_status "Step 3: Setting up application directory..."
APP_DIR="$HOME/chatbot"
mkdir -p $APP_DIR
cd $APP_DIR

# Step 4: Create virtual environment
print_status "Step 4: Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 5: Install Python packages
print_status "Step 5: Installing Python packages..."
pip install --upgrade pip
pip install flask flask-cors gunicorn
pip install scikit-learn numpy requests
pip install boto3  # For AWS Bedrock

# Step 6: Create requirements.txt if not exists
if [ ! -f requirements.txt ]; then
    print_status "Creating requirements.txt..."
    cat > requirements.txt << EOF
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
scikit-learn==1.3.2
numpy==1.26.2
requests==2.31.0
boto3==1.34.0
EOF
fi

# Step 7: Create systemd service
print_status "Step 7: Creating systemd service..."
sudo tee /etc/systemd/system/chatbot.service > /dev/null << EOF
[Unit]
Description=Smart Personal Assistant Chatbot
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app_web:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Step 8: Configure Nginx
print_status "Step 8: Configuring Nginx..."
sudo tee /etc/nginx/sites-available/chatbot > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/ubuntu/chatbot/static;
        expires 30d;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Step 9: Create log directory
print_status "Step 9: Creating log directory..."
mkdir -p $APP_DIR/logs

# Step 10: Set permissions
print_status "Step 10: Setting permissions..."
sudo chown -R $USER:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR

# Step 11: Start services
print_status "Step 11: Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot
sudo systemctl restart nginx

# Step 12: Check status
print_status "Step 12: Checking service status..."
sleep 3

if sudo systemctl is-active --quiet chatbot; then
    print_status "Chatbot service is running!"
else
    print_error "Chatbot service failed to start"
    sudo journalctl -u chatbot -n 20
    exit 1
fi

if sudo systemctl is-active --quiet nginx; then
    print_status "Nginx is running!"
else
    print_error "Nginx failed to start"
    exit 1
fi

# Step 13: Display information
echo ""
echo "============================================================"
print_status "🎉 Deployment completed successfully!"
echo "============================================================"
echo ""
echo "📊 Service Status:"
sudo systemctl status chatbot --no-pager | head -n 5
echo ""
echo "🌐 Access your chatbot at:"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "📝 Useful commands:"
echo "   View logs: sudo journalctl -u chatbot -f"
echo "   Restart: sudo systemctl restart chatbot"
echo "   Stop: sudo systemctl stop chatbot"
echo "   Status: sudo systemctl status chatbot"
echo ""
echo "🔧 Next steps:"
echo "   1. Upload your application files to $APP_DIR"
echo "   2. Restart service: sudo systemctl restart chatbot"
echo "   3. Configure domain name (optional)"
echo "   4. Setup SSL with: sudo certbot --nginx"
echo ""
print_status "Deployment script completed!"