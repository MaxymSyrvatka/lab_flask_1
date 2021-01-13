from flask import Flask, request, escape
from wsgiref.simple_server import make_server

app = Flask(__name__)


@app.route('/api/v1/hello-world-27')
def hello():
    name = request.args.get("name", "World 27")
    return f'Hello {escape(name)}'


server = make_server('', 8000, app)
print('http://127.0.0.1:8000/api/v1/hello-world-27')
server.serve_forever()
