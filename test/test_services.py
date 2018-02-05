import pytest
from . import load_up, load_down

from hello import app
from services import DBEvent, storage

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
storage.init_app(app)
app.app_context().push()
storage.db.create_all()
DBEvent.query.delete()


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()


def test_format(up):
    assert repr(storage) == "<DBStore with 0 events>"


def test_create_up(up):
    event = storage.create(up)
    assert event.alert_type == 2
    assert event.alert_name == 'Up'
    assert event.alert_duration == 99
    assert event.monitor_name == 'unittest'
    assert len(storage) == 1


def test_create_down(down):
    event = storage.create(down)
    assert event.alert_type == 1
    assert event.alert_name == 'Down'
    assert event.alert_duration == 5
    assert event.monitor_name == 'unittest'
    assert len(storage) == 2


def test_store(up, down):
    storage.create(down)
    storage.create(up)
    assert len(storage) == 4
    storage.flush(1)
    assert len(storage) == 1
    storage.flush(0)
    assert len(storage) == 0
    assert list(storage.select()) == []
