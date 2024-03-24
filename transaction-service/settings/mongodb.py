import os

MONGODB_NAME = os.getenv('MONGODB_NAME') or 'db'
MONGODB_HOST = os.getenv('MONGODB_HOST') or '0.0.0.0'
MONGODB_PORT = os.getenv('MONGODB_PORT') or '27017'
