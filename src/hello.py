from flask import Flask

from settings import VERSION


app = Flask(__name__)


@app.route('/')
def index():
    return 'Uptimerobot proxy'


@app.route('/version')
def version():
    return VERSION
