import pytest
from . import load_up, load_down

from services import trigger_event


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()


def test_format(up):
    assert "{}".format(trigger_event(up)) == "<Event (2) for unittest: Up since 99>"


def test_trigger_up(up):
    event = trigger_event(up)
    assert event.alert_type == 2
    assert event.alert_name == 'Up'
    assert event.alert_duration == 99
    assert event.monitor_name == 'unittest'


def test_trigger_down(down):
    event = trigger_event(down)
    assert event.alert_type == 1
    assert event.alert_name == 'Down'
    assert event.alert_duration == 5
    assert event.monitor_name == 'unittest'
