from mongoengine import connect
from account_service.api.app import app
from settings.app import *
from settings.mongodb import *

# MongoDB connection
connect(MONGODB_NAME, host=MONGODB_HOST, port=int(MONGODB_PORT))

if __name__ == '__main__':
    app.run(host=SANIC_APP_HOST, port=int(SANIC_APP_PORT), debug=DEBUG, auto_reload=DEBUG)
