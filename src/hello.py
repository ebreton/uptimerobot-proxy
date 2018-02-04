from flask import Flask, request, render_template, redirect, flash, url_for
from utils import import_class_from_string

from settings import VERSION, APP_SECRET, STORAGE_TYPE, DATABASE_URL

app = Flask(__name__)

# config app
app.secret_key = APP_SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL


def get_db(app):
    """ DB are usually not really relevant for proxies...

    However, one could like to know what is proxyed... The app therefore support
    - a pure python storage of the events received, lightning fast
    - or a more regular database through SQLAlchemy.

    The choice is made at runtime through environment variable STORAGE_TYPE:
    - in-memory storage with 'models.Store'
    - or real DB with 'services.db'
    """
    db_type = import_class_from_string(STORAGE_TYPE)
    initialized = db_type.init_app(app)
    return initialized if initialized is not None else db_type


# initialize DB
db = get_db(app)


@app.route('/')
def index():
    return render_template("list.html", events=db.select())


@app.route('/add', methods=['GET', 'POST'])
def add():
    event = db.create(request.args)
    return f"Stored {event}"


@app.route('/flush/<int:size>')
def flush(size):
    flash('flushed {} events'.format(max(0, len(db)-size)))
    db.flush(size)
    return redirect(url_for('index'))


@app.route('/version')
def version():
    flash(VERSION)
    return redirect(url_for('index'))
