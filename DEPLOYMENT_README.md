# 🚀 Complete AWS EC2 Deployment Package

Everything you need to deploy Smart Personal Assistant on AWS EC2 with Ubuntu

---

## 📦 **What's Included**

### **Documentation**
- `deploy_ec2_guide.md` - Complete step-by-step deployment guide
- `ec2_quick_start.md` - Quick 5-step deployment guide
- `DEPLOYMENT_README.md` - This file

### **Scripts**
- `deploy_to_ec2.sh` - Automated Ubuntu setup script (run on EC2)
- `upload_to_ec2.sh` - Upload files from local to EC2 (Linux/Mac)
- `DEPLOY_TO_EC2.bat` - Upload files from Windows to EC2

### **Application Files**
- `app_web.py` - Web version of chatbot (Flask)
- `enhanced_web_app.py` - Enhanced web version
- All Python modules and data files

---

## ⚡ **Quick Start (Choose Your Path)**

### **Path A: Automated Deployment (Recommended)**

**Time: ~20 minutes**

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.medium or t2.micro
   - Open ports: 22, 80, 5000

2. **Connect to EC2**
   ```bash
   ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP
   ```

3. **Run Deployment Script**
   ```bash
   # Download and run
   wget https://raw.githubusercontent.com/yourusername/yourrepo/main/deploy_to_ec2.sh
   chmod +x deploy_to_ec2.sh
   ./deploy_to_ec2.sh
   ```

4. **Upload Files**
   ```bash
   # From your Windows machine
   # Edit DEPLOY_TO_EC2.bat with your EC2 IP and key path
   # Then double-click DEPLOY_TO_EC2.bat
   ```

5. **Access Chatbot**
   ```
   http://YOUR_EC2_PUBLIC_IP
   ```

### **Path B: Manual Deployment**

**Time: ~30 minutes**

Follow the detailed guide in `deploy_ec2_guide.md`

### **Path C: Git-Based Deployment**

**Time: ~15 minutes**

1. Push code to GitHub
2. Run deployment script on EC2
3. Clone repo on EC2
4. Restart service

---

## 🎯 **Prerequisites**

### **AWS Requirements**
- [ ] AWS Account with EC2 access
- [ ] EC2 Key Pair created
- [ ] Basic AWS knowledge

### **Local Requirements**
- [ ] SSH client (built-in on Windows 10+)
- [ ] SCP for file transfer
- [ ] Your chatbot files ready

### **EC2 Instance Requirements**
- [ ] Ubuntu 22.04 LTS
- [ ] Minimum: t2.micro (1GB RAM)
- [ ] Recommended: t2.medium (4GB RAM)
- [ ] 20GB EBS storage

---

## 📋 **Deployment Checklist**

### **Before Deployment**
- [ ] AWS account created
- [ ] EC2 instance launched
- [ ] Security group configured
- [ ] Key pair downloaded
- [ ] Can SSH into instance

### **During Deployment**
- [ ] System updated
- [ ] Dependencies installed
- [ ] Virtual environment created
- [ ] Application files uploaded
- [ ] Services configured
- [ ] Nginx setup complete

### **After Deployment**
- [ ] Service running
- [ ] Can access via browser
- [ ] Chatbot responds correctly
- [ ] All features working
- [ ] Logs accessible

### **Production Ready**
- [ ] Domain name configured (optional)
- [ ] SSL certificate installed
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Auto-restart configured

---

## 🔧 **Configuration Files**

### **1. Systemd Service** (`/etc/systemd/system/chatbot.service`)

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
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### **2. Nginx Configuration** (`/etc/nginx/sites-available/chatbot`)

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/chatbot/static;
    }
}
```

---

## 💰 **Cost Breakdown**

### **Monthly Costs**

| Component | Free Tier | After Free Tier |
|-----------|-----------|-----------------|
| t2.micro | $0 (750 hrs) | ~$8/month |
| t2.small | N/A | ~$17/month |
| t2.medium | N/A | ~$34/month |
| EBS 20GB | $0 (30GB) | ~$2/month |
| Data Transfer | $0 (15GB) | $0.09/GB |
| **Total** | **$0** | **$10-40/month** |

### **Cost Optimization Tips**

1. **Use Free Tier** - t2.micro for first 12 months
2. **Stop When Not Needed** - Stop instance to save costs
3. **Reserved Instances** - Save 30-70% for 24/7 usage
4. **Monitor Usage** - Set billing alerts

---

## 🔒 **Security Best Practices**

### **1. SSH Security**
```bash
# Restrict SSH to your IP only
# AWS Console > Security Groups > Edit Inbound Rules
# SSH (22) - My IP
```

### **2. Firewall Setup**
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### **3. Regular Updates**
```bash
# Setup automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### **4. SSL Certificate**
```bash
# Free SSL with Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

---

## 📊 **Monitoring & Maintenance**

### **Check Service Health**
```bash
# Service status
sudo systemctl status chatbot

# View logs
sudo journalctl -u chatbot -f

# Check resources
htop
df -h
```

### **Update Application**
```bash
cd ~/chatbot
# Upload new files or git pull
sudo systemctl restart chatbot
```

### **Backup Data**
```bash
# Backup important files
tar -czf backup-$(date +%Y%m%d).tar.gz \
    assistant_data.json \
    smart_assistant.db \
    dataset.json

# Upload to S3 (optional)
aws s3 cp backup-*.tar.gz s3://your-bucket/backups/
```

---

## 🚨 **Troubleshooting Guide**

### **Service Won't Start**
```bash
# Check logs
sudo journalctl -u chatbot -n 50

# Test manually
cd ~/chatbot
source venv/bin/activate
python3 app_web.py
```

### **Can't Access from Browser**
```bash
# Check security group
# Check service is running
sudo systemctl status chatbot

# Check Nginx
sudo systemctl status nginx

# Test locally
curl http://localhost:5000
```

### **502 Bad Gateway**
```bash
# Restart chatbot service
sudo systemctl restart chatbot

# Check if port 5000 is in use
sudo netstat -tulpn | grep 5000
```

### **Out of Memory**
```bash
# Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 🎓 **Learning Resources**

### **AWS Documentation**
- [EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [EC2 Pricing](https://aws.amazon.com/ec2/pricing/)
- [Free Tier](https://aws.amazon.com/free/)

### **Ubuntu Server**
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Systemd Documentation](https://systemd.io/)

### **Web Deployment**
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## 🎉 **Success!**

Your Smart Personal Assistant is now deployed on AWS EC2!

### **What You've Achieved**
✅ Professional cloud deployment
✅ Production-ready setup
✅ Scalable architecture
✅ Secure configuration
✅ Monitoring and logging
✅ Auto-restart on failure

### **Next Steps**
1. Configure custom domain
2. Setup SSL certificate
3. Implement CI/CD pipeline
4. Add monitoring alerts
5. Setup automated backups

---

## 📞 **Support**

### **Common Commands**
```bash
# Service management
sudo systemctl start|stop|restart|status chatbot

# View logs
sudo journalctl -u chatbot -f

# Update code
cd ~/chatbot && git pull && sudo systemctl restart chatbot

# Check resources
htop
df -h
free -h
```

### **Need Help?**
- Check `deploy_ec2_guide.md` for detailed instructions
- Check `ec2_quick_start.md` for quick reference
- Review logs: `sudo journalctl -u chatbot -f`

---

**Happy Deploying! 🚀**