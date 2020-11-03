from flask import Flask
from wsgiref.simple_server import make_server

app = Flask(__name__)


@app.route('/api/v1/hello-world-27')
def hello():
    return 'Hello World 27'


server = make_server('', 8000, app)
server.serve_forever()
