import os

DEBUG = os.getenv('DEBUG') in ['true', 'True']
SANIC_APP_HOST = os.getenv('HOST') or '0.0.0.0'
SANIC_APP_PORT = os.getenv('PORT') or '8000'
