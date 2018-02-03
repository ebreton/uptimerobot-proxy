import pytest
from flask import url_for

from hello import app
from settings import VERSION

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


def test_version():
    with app.test_client() as client:
        resp = client.get('/version')
        assert resp.get_data() == bytes(VERSION, encoding='utf8')


def test_index_listing(up, down):
    with app.test_client() as client:
        client.post('/add', query_string=up)
        client.post('/add', query_string=down)
        client.post('/add', query_string=up)
        assert client.get('/').get_data() == b"3 events received"
