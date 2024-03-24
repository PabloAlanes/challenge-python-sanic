import os

ACCOUNT_SVC_ENABLED = os.getenv('ACCOUNT_SVC_ENABLED') in ['true', 'True'] or False
ACCOUNT_SVC_URL = os.getenv('ACCOUNT_SVC_URL') or 'http://0.0.0.0:8000'
TRANSACTION_SVC_URL = os.getenv('TRANSACTION_SVC_URL') or 'http://0.0.0.0:8000'
