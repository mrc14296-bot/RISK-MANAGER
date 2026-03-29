#!/bin/bash
# Google Cloud Ubuntu Deploy Script for MindRiskControl
# Usage: ./deploy.sh [server_ip] [ssh_user] [key_path]
# Example: ./deploy.sh 34.123.45.67 ubuntu ~/.ssh/google_compute_engine

set -e

SERVER_IP=${1:-\"your-vm-external-ip\"}
SSH_USER=${2:-\"ubuntu\"}
KEY_PATH=${3:-\"\~/.ssh/google_compute_engine\"}
APP_DIR=\"/var/www/mindriskcontrol\"
VENV_DIR=\"$APP_DIR/venv\"

echo \"🚀 Deploying to $SERVER_IP as $SSH_USER...\"

# 1. Create temp dir local
mkdir -p tmp-deploy
tar -czf tmp-deploy/project.tar.gz -C . --exclude=\".git\" --exclude=\"tmp-deploy\" --exclude=\"*.pyc\" .

# 2. SSH and setup
scp -i \"$KEY_PATH\" -r tmp-deploy/project.tar.gz $SSH_USER@$SERVER_IP:$HOME/
scp -i \"$KEY_PATH\" $KEY_PATH.pub $SSH_USER@$SERVER_IP:~/.ssh/authorized_keys 2>/dev/null || true

ssh -i \"$KEY_PATH\" $SSH_USER@$SERVER_IP << EOF
echo \"📁 Setting up $APP_DIR...\"
sudo mkdir -p $APP_DIR /var/lib/flask /var/log/mindriskcontrol
sudo chown -R www-data:www-data $APP_DIR /var/lib/flask /var/log/mindriskcontrol

cd ~
tar -xzf project.tar.gz -C $APP_DIR --strip-components=1

# Virtualenv & deps
cd $APP_DIR
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip nginx supervisor

python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configs
sudo cp gunicorn.service /etc/systemd/system/
sudo cp nginx-mindriskcontrol.conf /etc/nginx/sites-available/mindriskcontrol
sudo ln -sf /etc/nginx/sites-available/mindriskcontrol /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-enabled/default.old 2>/dev/null || true

# DB init
sudo mkdir -p /var/lib/flask
sudo chown www-data:www-data /var/lib/flask
source venv/bin/activate
python3 -c \"
from app import app, db
with app.app_context():
    db.create_all()
print('✅ DB tables created')
\"

# Services
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

sudo nginx -t
sudo systemctl reload nginx

echo \"✅ Deploy complete!\"
echo \"Logs: journalctl -u gunicorn -f\"
echo \"Nginx: tail -f /var/log/nginx/error.log\"
echo \"Test: curl localhost:8000/debug-status\"
echo \"Site: http://$SERVER_IP\"
EOF

rm -rf tmp-deploy
echo \"🎉 Deploy finished! Check server logs for 502 fix.\"

