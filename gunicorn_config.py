import multiprocessing
import os

# Número de workers baseado no número de cores
workers = multiprocessing.cpu_count() * 2 + 1

# Tempo limite de resposta em segundos
timeout = 120

# Máximo de requisições antes do worker ser reiniciado
max_requests = 1000
max_requests_jitter = 50

# Configurações de logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Configurações de buffer
worker_class = 'gevent'
worker_connections = 2000

# Bind to Heroku's dynamic port
bind = f"0.0.0.0:{int(os.environ.get('PORT', 5000))}"