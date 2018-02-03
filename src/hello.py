from flask import Flask, request

from services import trigger_event
from settings import VERSION

app = Flask(__name__)
store = []


@app.route('/')
def index():
    return '{} events received'.format(len(store))


@app.route('/version')
def version():
    return VERSION


@app.route('/add', methods=['POST'])
def add():
    event = trigger_event(request.args)
    store.append(event)
    return "Stored {}".format(event)
