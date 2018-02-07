import pytest
import json
from . import load_up, load_down

from models import Event, storage
from settings import E2EMONITORING_SERVICE, E2EMONITORING_DOWN, E2EMONITORING_UP


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()


def test_format(up):
    assert repr(Event.create_event(up)) == "<Event (2) for unittest: Up since 0:00:00>"


def test_create_up(up):
    event = Event.create_event(up)
    assert event.alert_type == 2
    assert event.alert_name == 'Up'
    assert event.alert_duration.seconds == 0
    assert event.monitor_name == 'unittest'


def test_create_down(down):
    event = Event.create_event(down)
    assert event.alert_type == 1
    assert event.alert_name == 'Down'
    assert event.alert_duration.seconds == 5
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


def test_to_json_up(up):
    assert json.loads(Event.create_event(up).to_json()) == {
        "u_business_service": E2EMONITORING_SERVICE,
        "u_priority": E2EMONITORING_UP,
        "u_short_description": "unittest is Up",
        "u_description": "unittest is Up (for testing purpose). It was down for 4 minutes and 39 seconds.",
    }


def test_to_json_down(down):
    assert json.loads(Event.create_event(down).to_json()) == {
        "u_business_service": E2EMONITORING_SERVICE,
        "u_priority": E2EMONITORING_DOWN,
        "u_short_description": "unittest is Down",
        "u_description": "unittest is Down: for testing purpose.",
    }
