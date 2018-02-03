from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/hello/<username>')
def user(username='World'):
    return 'Hello, {}'.format(username)
