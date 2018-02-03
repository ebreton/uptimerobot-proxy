from flask import Flask, request, render_template, redirect, flash, url_for

from models import Store
from services import trigger_event
from settings import VERSION

app = Flask(__name__)

# set secret to create secured sessions
app.secret_key = 'some_secret'

# storage in memory for this first version
storage = Store()


@app.route('/')
def index():
    return render_template("list.html", events=storage.store)


@app.route('/add', methods=['GET', 'POST'])
def add():
    event = trigger_event(request.args)
    storage.insert(event)
    return "Stored {}".format(event)


@app.route('/flush/<int:size>')
def flush(size):
    flash('flushed {} events'.format(max(0, len(storage)-size)))
    storage.flush(size)
    return redirect(url_for('index'))


@app.route('/version')
def version():
    flash(VERSION)
    return redirect(url_for('index'))
