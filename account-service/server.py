from sanic import Sanic
from sanic.response import text
from mongoengine import connect
from settings.app import *
from settings.mongodb import *

# MongoDB connection
connect(MONGODB_NAME, host=MONGODB_HOST, port=int(MONGODB_PORT))

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")

if __name__ == '__main__':
    app.run(host=SANIC_APP_HOST, port=int(SANIC_APP_PORT), debug=DEBUG, auto_reload=DEBUG)
