import pytest
from . import load_up, load_down

from hello import create_app

app, storage = create_app(storage_type="models.storage")
app.app_context().push()
storage.init_db()


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()


def test_format(up):
    assert repr(storage) == "<DBStore with 0 events>"


def test_create_up(up):
    db_event = storage.create(up)
    assert db_event.alert_type == 2
    assert db_event.alert_name == 'Up'
    assert db_event.alert_duration == 99
    assert db_event.monitor_name == 'unittest'
    assert len(storage) == 1


def test_create_down(down):
    db_event = storage.create(down)
    assert db_event.alert_type == 1
    assert db_event.alert_name == 'Down'
    assert db_event.alert_duration == 0
    assert db_event.monitor_name == 'unittest'
    assert len(storage) == 2


def test_store_create(up, down):
    storage.create(down)
    storage.create(up)
    assert repr(storage) == '<DBStore with 4 events>'
    assert len(storage) == 4


def test_store_flush():
    storage.flush(1)
    assert len(storage) == 1
    storage.flush(0)
    storage.flush(2)
    assert len(storage) == 0


def test_store_select(down):
    assert list(storage.select()) == []
    db_event = storage.create(down)
    assert list(storage.select()) == [db_event]
    storage.flush(0)


def test_store_get(up):
    db_event = storage.create(up)
    assert storage.get(db_event.id) == db_event
    storage.flush(0)
