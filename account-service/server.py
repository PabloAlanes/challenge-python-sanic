import os
from sanic import Sanic
from sanic.response import text


DEBUG = os.getenv('DEBUG') in ['true', 'True']
SANIC_APP_HOST = os.getenv('HOST') or '0.0.0.0'
SANIC_APP_PORT = os.getenv('PORT') or '8000'

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")

if __name__ == '__main__':
    app.run(host=SANIC_APP_HOST, port=int(SANIC_APP_PORT), debug=DEBUG, auto_reload=DEBUG)
