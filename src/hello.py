from flask import Flask, request, render_template, redirect, flash, url_for
from utils import import_class_from_string

from services import Proxy
from settings import VERSION, APP_SECRET, STORAGE_TYPE, DATABASE_URL, UPTIMEROBOT_UP


def create_app(storage_type=STORAGE_TYPE):
    """ DB are usually not really relevant for proxies...

    However, one could like to know what is proxyed... The app therefore support
    - a pure python storage of the events received, lightning fast
    - or a more regular database through SQLAlchemy.

    The choice is made at runtime through environment variable STORAGE_TYPE:
    - in-memory storage with 'entities.storage'
    - or real DB with 'models.storage'
    """
    app = Flask(__name__)
    # config app
    app.secret_key = APP_SECRET
    # config storage
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_type = import_class_from_string(storage_type)
    db_type.init_app(app)
    return app, db_type


app, storage = create_app()


@app.template_filter('e2em')
def to_json(event):
    return Proxy().event_to_json(event)


@app.route('/')
def index():
    return render_template("list.html", events=storage.select())


@app.route('/add', methods=['GET', 'POST'])
def add():
    event = storage.create(request.args)
    Proxy().forward(event)
    return f"Stored & forwarded {event}"


@app.route('/forward/<int:event_id>')
def forward(event_id):
    event = storage.get(event_id)
    if event.alert_type != UPTIMEROBOT_UP:
        flash(f'only alerts Up can be forwarded, not {event.alert_name}')
    else:
        Proxy().forward(event)
        flash(f'forwarded {event}')
    return redirect(url_for('index'))


@app.route('/flush/<int:size>')
def flush(size):
    flash('flushed {} events'.format(max(0, len(storage)-size)))
    storage.flush(size)
    return redirect(url_for('index'))


@app.route('/version')
def version():
    flash(VERSION)
    return redirect(url_for('index'))
