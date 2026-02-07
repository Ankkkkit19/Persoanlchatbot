# 🚀 AWS EC2 Deployment Guide - Ubuntu

Complete guide to deploy Smart Personal Assistant on AWS EC2 with Ubuntu

---

## 📋 **Prerequisites**

1. **AWS Account** with EC2 access
2. **SSH Key Pair** for EC2 instance
3. **Basic Linux knowledge**
4. **Domain name** (optional, for production)

---

## 🖥️ **Step 1: Launch EC2 Instance**

### **1.1 Create EC2 Instance**

```bash
# AWS Console Steps:
1. Go to EC2 Dashboard
2. Click "Launch Instance"
3. Choose Ubuntu Server 22.04 LTS (Free tier eligible)
4. Instance Type: t2.medium (recommended) or t2.micro (free tier)
5. Configure Security Group:
   - SSH (22) - Your IP
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom TCP (5000) - 0.0.0.0/0 (for Flask)
6. Create/Select Key Pair
7. Launch Instance
```

### **1.2 Connect to Instance**

```bash
# Windows (PowerShell/CMD)
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

# Linux/Mac
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip
```

---

## 🔧 **Step 2: Setup Ubuntu Server**

### **2.1 Update System**

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor
```

### **2.2 Install Python Dependencies**

```bash
# Create application directory
mkdir -p ~/chatbot
cd ~/chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install --upgrade pip
pip install flask flask-cors gunicorn
pip install scikit-learn numpy requests
pip install boto3  # For AWS Bedrock (optional)
```

---

## 📦 **Step 3: Deploy Application**

### **3.1 Upload Files to EC2**

```bash
# From your local machine (Windows)
# Option 1: Using SCP
scp -i "your-key.pem" -r C:\path\to\your\chatbot\* ubuntu@your-ec2-ip:~/chatbot/

# Option 2: Using Git (Recommended)
# On EC2:
cd ~/chatbot
git clone https://github.com/yourusername/your-repo.git .
# OR upload via GitHub/GitLab
```

### **3.2 Create Web Application**

The web version is already created in `enhanced_web_app.py` and `app_web.py`.
We'll use the enhanced version for deployment.

---

## 🌐 **Step 4: Configure Web Server**

### **4.1 Create Gunicorn Service**

```bash
# Create systemd service file
sudo nano /etc/systemd/system/chatbot.service
```

**Add this content:**

```ini
[Unit]
Description=Smart Personal Assistant Chatbot
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/chatbot
Environment="PATH=/home/ubuntu/chatbot/venv/bin"
ExecStart=/home/ubuntu/chatbot/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app_web:app

[Install]
WantedBy=multi-user.target
```

**Save and enable:**

```bash
sudo systemctl daemon-reload
sudo systemctl start chatbot
sudo systemctl enable chatbot
sudo systemctl status chatbot
```

### **4.2 Configure Nginx**

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/chatbot
```

**Add this content:**

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or EC2 public IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/ubuntu/chatbot/static;
    }
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 **Step 5: Setup SSL (Optional but Recommended)**

### **5.1 Install Certbot**

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### **5.2 Get SSL Certificate**

```bash
sudo certbot --nginx -d your-domain.com
```

---

## 🧪 **Step 6: Test Deployment**

### **6.1 Check Services**

```bash
# Check chatbot service
sudo systemctl status chatbot

# Check Nginx
sudo systemctl status nginx

# View logs
sudo journalctl -u chatbot -f
```

### **6.2 Access Application**

```bash
# Open in browser:
http://your-ec2-public-ip
# OR
https://your-domain.com
```

---

## 📊 **Step 7: Monitoring & Maintenance**

### **7.1 Setup Logging**

```bash
# Create log directory
mkdir -p ~/chatbot/logs

# View application logs
tail -f ~/chatbot/logs/app.log

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **7.2 Auto-restart on Failure**

```bash
# Edit service file
sudo nano /etc/systemd/system/chatbot.service
```

**Add restart policy:**

```ini
[Service]
Restart=always
RestartSec=10
```

### **7.3 Setup Monitoring**

```bash
# Install monitoring tools
sudo apt install -y htop iotop

# Monitor resources
htop
```

---

## 🔄 **Step 8: Update Application**

### **8.1 Update Code**

```bash
cd ~/chatbot
source venv/bin/activate

# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart chatbot
```

### **8.2 Backup Data**

```bash
# Backup database and data files
tar -czf backup-$(date +%Y%m%d).tar.gz assistant_data.json smart_assistant.db

# Upload to S3 (optional)
aws s3 cp backup-*.tar.gz s3://your-bucket/backups/
```

---

## 💰 **Cost Estimation**

### **EC2 Instance Costs (Monthly)**

- **t2.micro** (Free tier): $0 (first 12 months)
- **t2.small**: ~$17/month
- **t2.medium**: ~$34/month

### **Additional Costs**

- **Data Transfer**: ~$0.09/GB (first 10TB)
- **EBS Storage**: ~$0.10/GB-month
- **Elastic IP**: Free if attached to running instance

### **Total Estimated Cost**

- **Development**: $0-20/month (free tier)
- **Production**: $35-50/month (t2.medium + extras)

---

## 🚨 **Troubleshooting**

### **Common Issues**

**1. Service won't start:**
```bash
sudo journalctl -u chatbot -n 50
# Check for Python errors
```

**2. Nginx 502 Bad Gateway:**
```bash
# Check if chatbot service is running
sudo systemctl status chatbot
# Check port 5000
sudo netstat -tulpn | grep 5000
```

**3. Permission denied:**
```bash
# Fix permissions
sudo chown -R ubuntu:www-data ~/chatbot
sudo chmod -R 755 ~/chatbot
```

**4. Out of memory:**
```bash
# Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 🎯 **Production Checklist**

- [ ] EC2 instance launched and configured
- [ ] Security groups properly configured
- [ ] Application deployed and running
- [ ] Nginx configured as reverse proxy
- [ ] SSL certificate installed
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Auto-restart configured
- [ ] Logs properly configured
- [ ] Domain name configured (if applicable)

---

## 📚 **Additional Resources**

- **AWS EC2 Documentation**: https://docs.aws.amazon.com/ec2/
- **Nginx Documentation**: https://nginx.org/en/docs/
- **Gunicorn Documentation**: https://docs.gunicorn.org/
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/

---

## 🎉 **Success!**

Your Smart Personal Assistant is now deployed on AWS EC2!

**Access your chatbot at:**
- HTTP: `http://your-ec2-ip`
- HTTPS: `https://your-domain.com`

**Next Steps:**
1. Configure domain name
2. Setup monitoring alerts
3. Implement CI/CD pipeline
4. Scale with load balancer (if needed)