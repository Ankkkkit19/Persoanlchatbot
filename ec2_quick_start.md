# ⚡ EC2 Quick Start Guide

Fast deployment guide for Smart Personal Assistant on AWS EC2 Ubuntu

---

## 🚀 **Quick Deployment (5 Steps)**

### **Step 1: Launch EC2 Instance (5 minutes)**

1. Go to AWS EC2 Console
2. Click **"Launch Instance"**
3. Select **Ubuntu Server 22.04 LTS**
4. Choose **t2.medium** (or t2.micro for testing)
5. Configure Security Group:
   - SSH (22) - Your IP
   - HTTP (80) - Anywhere
   - Custom TCP (5000) - Anywhere
6. Create/Download Key Pair
7. Launch!

### **Step 2: Connect to EC2 (2 minutes)**

```bash
# Windows PowerShell
ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP

# If permission error on Windows:
icacls "your-key.pem" /inheritance:r
icacls "your-key.pem" /grant:r "%username%:R"
```

### **Step 3: Run Deployment Script (10 minutes)**

```bash
# On EC2 instance
wget https://raw.githubusercontent.com/yourusername/yourrepo/main/deploy_to_ec2.sh
chmod +x deploy_to_ec2.sh
./deploy_to_ec2.sh
```

### **Step 4: Upload Your Files (5 minutes)**

**Option A: Using SCP (from your Windows machine)**

```bash
# Edit upload_to_ec2.sh with your EC2 IP and key path
# Then run:
bash upload_to_ec2.sh
```

**Option B: Using Git**

```bash
# On EC2:
cd ~/chatbot
git clone https://github.com/yourusername/yourrepo.git .
sudo systemctl restart chatbot
```

**Option C: Manual Upload**

```bash
# From Windows PowerShell:
scp -i "your-key.pem" app_web.py ubuntu@YOUR_EC2_IP:~/chatbot/
scp -i "your-key.pem" chatbot.py ubuntu@YOUR_EC2_IP:~/chatbot/
# ... upload all files
```

### **Step 5: Access Your Chatbot (1 minute)**

```bash
# Open in browser:
http://YOUR_EC2_PUBLIC_IP
```

---

## 🎯 **Essential Commands**

### **Service Management**

```bash
# Start chatbot
sudo systemctl start chatbot

# Stop chatbot
sudo systemctl stop chatbot

# Restart chatbot
sudo systemctl restart chatbot

# Check status
sudo systemctl status chatbot

# View logs
sudo journalctl -u chatbot -f
```

### **Update Application**

```bash
cd ~/chatbot
# Upload new files or git pull
sudo systemctl restart chatbot
```

### **Check if Running**

```bash
# Check service
sudo systemctl is-active chatbot

# Check port
sudo netstat -tulpn | grep 5000

# Test locally
curl http://localhost:5000
```

---

## 🔧 **Troubleshooting**

### **Service won't start**

```bash
# View detailed logs
sudo journalctl -u chatbot -n 50 --no-pager

# Check Python errors
cd ~/chatbot
source venv/bin/activate
python3 app_web.py
```

### **Can't access from browser**

```bash
# Check security group allows port 80
# Check Nginx is running
sudo systemctl status nginx

# Check firewall
sudo ufw status
```

### **502 Bad Gateway**

```bash
# Chatbot service not running
sudo systemctl restart chatbot

# Check if port 5000 is in use
sudo lsof -i :5000
```

---

## 💰 **Cost Optimization**

### **Free Tier (First 12 Months)**

- **t2.micro**: 750 hours/month FREE
- **30 GB EBS**: FREE
- **15 GB data transfer**: FREE

### **After Free Tier**

- **t2.micro**: ~$8/month
- **t2.small**: ~$17/month
- **t2.medium**: ~$34/month

### **Save Money**

```bash
# Stop instance when not in use
aws ec2 stop-instances --instance-ids i-xxxxx

# Start when needed
aws ec2 start-instances --instance-ids i-xxxxx

# Use Reserved Instances for 24/7 usage (save 30-70%)
```

---

## 🔒 **Security Best Practices**

### **1. Restrict SSH Access**

```bash
# Edit security group to allow SSH only from your IP
# AWS Console > EC2 > Security Groups > Edit Inbound Rules
```

### **2. Setup Firewall**

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### **3. Regular Updates**

```bash
sudo apt update && sudo apt upgrade -y
```

### **4. Setup SSL (Free)**

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (requires domain name)
sudo certbot --nginx -d yourdomain.com
```

---

## 📊 **Monitoring**

### **Check Resources**

```bash
# CPU and Memory
htop

# Disk usage
df -h

# Service logs
sudo journalctl -u chatbot -f
```

### **Setup Alerts**

```bash
# AWS CloudWatch (free tier: 10 alarms)
# Set alerts for:
# - CPU > 80%
# - Memory > 80%
# - Disk > 80%
```

---

## 🎉 **Success Checklist**

- [ ] EC2 instance running
- [ ] Can SSH into instance
- [ ] Deployment script completed
- [ ] Files uploaded
- [ ] Service running: `sudo systemctl status chatbot`
- [ ] Nginx running: `sudo systemctl status nginx`
- [ ] Can access via browser: `http://YOUR_EC2_IP`
- [ ] Chatbot responds to questions
- [ ] All features working

---

## 📞 **Need Help?**

### **Common Issues**

1. **"Permission denied" for key file**
   - Windows: Run `icacls` commands above
   - Linux/Mac: Run `chmod 400 your-key.pem`

2. **"Connection refused"**
   - Check security group allows your IP
   - Check instance is running

3. **"502 Bad Gateway"**
   - Service not running: `sudo systemctl start chatbot`
   - Check logs: `sudo journalctl -u chatbot -f`

4. **"Module not found"**
   - Activate venv: `source ~/chatbot/venv/bin/activate`
   - Install packages: `pip install -r requirements.txt`

---

## 🚀 **Next Steps**

1. **Get Domain Name** (optional)
   - Register domain (Namecheap, GoDaddy, etc.)
   - Point to EC2 IP
   - Setup SSL with Certbot

2. **Setup Monitoring**
   - CloudWatch alarms
   - Log aggregation
   - Performance monitoring

3. **Implement CI/CD**
   - GitHub Actions
   - Automatic deployment
   - Testing pipeline

4. **Scale Up**
   - Load balancer
   - Auto-scaling
   - Database (RDS)

---

**Your chatbot is now live on AWS EC2! 🎉**