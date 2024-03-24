import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST') or '0.0.0.0'
RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER') or 'guest'
RABBITMQ_PASS = os.getenv('RABBITMQ_DEFAULT_USER') or 'guest'
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE') or 'task_queue'
RABBITMQ_ENABLED = os.getenv('RABBITMQ_ENABLED') in ['true', 'True'] or False
