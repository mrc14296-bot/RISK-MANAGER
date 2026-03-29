# 🚀 Google Cloud Ubuntu Nginx 502 Bad Gateway Fix - Production Deploy
Status: 📋 Step 1/9 Complete - TODO Created ✅

## Project Context
Flask trading app runs locally perfect → 502 on Google Cloud SSH Ubuntu server (nginx/1.18.0).
**Root Causes**: SQLite DB write fail, no production gunicorn service, port mismatch.

## Approved Plan Steps (Execute Sequentially)

### ✅ 1. Create TODO-GC-502.md (Progress Tracking) - **COMPLETE**

### ✅ 2. Update app.py - Production DB `/var/lib/flask/users.db`, safe @app.before_first_request init, $PORT/debug env

### ⏳ 3. Create gunicorn.conf.py - Reliable Production Config
   ```
   bind = \"127.0.0.1:8000\"
   workers = 3
   timeout = 120
   loglevel = \"info\"
   ```

### ⏳ 4. Create gunicorn.service - Systemd Auto-Restart Service
   - Runs as www-data, venv, restart=always
   - `/etc/systemd/system/gunicorn.service`

### ✅ 5. Create nginx-mindriskcontrol.conf - upstream flask_app:8000, static cache, security headers

### ✅ 6. Create deploy.sh - scp tar, venv, pip, DB init, systemctl enable gunicorn/nginx
   - scp files, create venv, pip install, DB dir, systemctl enable

### ⏳ 7. Local Test - Gunicorn Production Mode
   ```
   mkdir -p /tmp/instance
   export DATABASE_URL=\"sqlite:////tmp/instance/users.db\"
   gunicorn --config gunicorn.conf.py --bind 0.0.0.0:8000 app:app
   # Test: curl localhost:8000/debug-status
   ```

### ⏳ 8. Server Deploy - User Executes
   ```
   chmod +x deploy.sh
   ./deploy.sh [server-ip] [ssh-user]
   ssh server: sudo systemctl daemon-reload && sudo systemctl enable --now gunicorn
   sudo nginx -t && sudo systemctl reload nginx
   ```

### ⏳ 9. Verify & Complete
   - Logs: `journalctl -u gunicorn -f`, `tail /var/log/nginx/error.log`
   - Test: site.com/debug-status → {\"database\": \"connected\"}
   - Success: 502 gone, full app works!

## Server Prerequisites (User Check)
```
Ubuntu 22.04+, nginx installed (`sudo apt install nginx`)
Python 3.10+ (`sudo apt install python3.10 python3.10-venv python3-pip`)
App dir: /var/www/mindriskcontrol (`sudo mkdir -p /var/www/mindriskcontrol`)
SSH access: gcloud compute ssh or ssh-key
Domain/IP points to VM public IP
```

## Current Progress: 1/9 ✅
**Next Step**: Update app.py DB path. Reply **\"NEXT\"** after file created successfully.

