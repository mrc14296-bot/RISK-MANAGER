"""
Production Gunicorn config for Google Cloud Ubuntu / Nginx setup
Place this in project root (/var/www/mindriskcontrol/gunicorn.conf.py)
"""

import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"  # Nginx proxies to this port
backlog = 2048

# Worker processes (CPU-based)
workers = max((multiprocessing.cpu_count() * 2 + 1), 3)
worker_class = "sync"
worker_connections = 1000

# Timeouts for Binance API calls
timeout = 120
keepalive = 2

# Restart workers after N requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
loglevel = "info"
accesslog = "-"  
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "mindriskcontrol"

# User/group (match nginx)
user = "www-data"
group = "www-data"

# Preload app (DB connections)
preload_app = True

# Graceful restart
graceful_timeout = 60

