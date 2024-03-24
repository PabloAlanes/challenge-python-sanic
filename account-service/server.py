import os
from sanic import Sanic
from sanic.response import text
from mongoengine import connect


DEBUG = os.getenv('DEBUG') in ['true', 'True']
SANIC_APP_HOST = os.getenv('HOST') or '0.0.0.0'
SANIC_APP_PORT = os.getenv('PORT') or '8000'
MONGODB_NAME = os.getenv('MONGODB_NAME') or 'db'
MONGODB_HOST = os.getenv('MONGODB_HOST') or '0.0.0.0'
MONGODB_PORT = os.getenv('MONGODB_PORT') or '27017'

# MongoDB connection
connect(MONGODB_NAME, host=MONGODB_HOST, port=int(MONGODB_PORT))

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")

if __name__ == '__main__':
    app.run(host=SANIC_APP_HOST, port=int(SANIC_APP_PORT), debug=DEBUG, auto_reload=DEBUG)
