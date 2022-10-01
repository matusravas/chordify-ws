from .controller import *


@router.route("/", methods=['GET'])
def hello_world():
    return "<p>Chordify WS. Hello World!</p>"


@router.route("/ping", methods=['GET'])
def hello_world():
    return {'data': 'Server running...'}