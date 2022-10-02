from .controller import *
from app import app


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Chordify WS. Hello World!</p>"


@app.route("/ping", methods=['GET'])
def ping():
    return {'data': 'Server running...'}