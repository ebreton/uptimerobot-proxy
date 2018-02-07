import pytest
import requests_mock
from flask import url_for

from hello import app, storage
from settings import E2EMONITORING_URL

from . import load_up, load_down

app.testing = True


@pytest.fixture
def up():
    return load_up()


@pytest.fixture
def down():
    return load_down()


def test_urls():
    with app.test_request_context():
        assert url_for('index') == '/'
        assert url_for('version') == '/version'


def test_storage(up, down):
    with app.test_client() as client, requests_mock.Mocker() as mocker:
        mocker.post(E2EMONITORING_URL, text='resp')
        assert len(storage) == 0
        client.post('/add', query_string=up)
        client.post('/add', query_string=down)
        client.post('/add', query_string=up)
        assert len(storage) == 3
        client.get('/flush/2')
        assert len(storage) == 2
