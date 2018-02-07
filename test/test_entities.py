import pytest
from . import load_up, load_down

from entities import Event, storage


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()


def test_format(down):
    assert repr(Event.create_event(down)) == "<Event for unittest: Down(1) since 0:00:00, for testing purpose>"


def test_create_up(up):
    event = Event.create_event(up)
    assert event.alert_type == 2
    assert event.alert_name == 'Up'
    assert event.alert_duration == 99
    assert event.monitor_name == 'unittest'


def test_create_down(down):
    event = Event.create_event(down)
    assert event.alert_type == 1
    assert event.alert_name == 'Down'
    assert event.alert_duration == 0
    assert event.monitor_name == 'unittest'


def test_store(up, down):
    storage.init_app(None)
    assert repr(storage) == '<Store with 0 events>'
    storage.insert(Event.create_event(down))
    storage.create(up)
    assert repr(storage) == '<Store with 2 events>'
    assert len(storage) == 2
    storage.flush(1)
    assert len(storage) == 1
    storage.flush(0)
    assert len(storage) == 0
    assert list(storage.select()) == []
