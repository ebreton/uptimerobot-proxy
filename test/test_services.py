import pytest
import json
from entities import Event
from services import Proxy

from settings import E2EMONITORING_SERVICE, E2EMONITORING_DOWN, E2EMONITORING_UP

from . import load_up, load_down

proxy = Proxy()


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()


def test_to_json_up(up):
    assert json.loads(proxy.event_to_json(Event.create_event(up))) == {
        "u_business_service": E2EMONITORING_SERVICE,
        "u_priority": E2EMONITORING_UP,
        "u_short_description": "unittest is Up",
        "u_description": "unittest is Up (for testing purpose). It was down for 0:01:39.",
    }


def test_to_json_down(down):
    assert json.loads(proxy.event_to_json(Event.create_event(down))) == {
        "u_business_service": E2EMONITORING_SERVICE,
        "u_priority": E2EMONITORING_DOWN,
        "u_short_description": "unittest is Down",
        "u_description": "unittest is Down: for testing purpose.",
    }
