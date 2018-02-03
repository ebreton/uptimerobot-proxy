import os
import json
import pytest

from services import trigger_event
from settings import TEST_PATH


@pytest.fixture
def up():
    file_path = os.path.join(TEST_PATH, 'event_up.json')
    with open(file_path) as input:
        return json.load(input)


@pytest.fixture
def down():
    file_path = os.path.join(TEST_PATH, 'event_down.json')
    with open(file_path) as input:
        return json.load(input)


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
