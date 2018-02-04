import pytest
from . import load_up, load_down


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()
