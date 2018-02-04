from flask import Flask, request, render_template, redirect, flash, url_for
from utils import import_class_from_string

from settings import VERSION, APP_SECRET, DB_CLASS, DB_URI

app = Flask(__name__)

# config app
app.secret_key = APP_SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI


def get_db(app):
    db_class = import_class_from_string(DB_CLASS)
    initialized = db_class.init_app(app)
    return initialized if initialized is not None else db_class


# initialize DB
db = get_db(app)


@app.route('/')
def index():
    return render_template("list.html", events=db.select())


@app.route('/add', methods=['GET', 'POST'])
def add():
    event = db.create(request.args)
    return "Stored {}".format(event)


@app.route('/flush/<int:size>')
def flush(size):
    flash('flushed {} events'.format(max(0, len(db)-size)))
    db.flush(size)
    return redirect(url_for('index'))


@app.route('/version')
def version():
    flash(VERSION)
    return redirect(url_for('index'))
