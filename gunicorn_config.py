import multiprocessing
import os

# Reduce number of workers to minimize memory usage
workers = 2  # Fixed number instead of dynamic calculation

# Tempo limite de resposta em segundos
timeout = 120

# Máximo de requisições antes do worker ser reiniciado
max_requests = 1000
max_requests_jitter = 50

# Configurações de logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Configurações de buffer e memory management
worker_class = 'gevent'
worker_connections = 1000
keepalive = 5

# Preload app to share memory
preload_app = True


# Bind to Heroku's dynamic port
bind = f"0.0.0.0:{int(os.environ.get('PORT', 5000))}"