from flask import url_for
from hello import app

from settings import VERSION


def test_urls():
    with app.test_request_context():
        assert url_for('index') == '/'
        assert url_for('version') == '/version'


def test_version():
    with app.test_client() as client:
        resp = client.get('/version')
        assert resp.get_data() == bytes(VERSION, encoding='utf8')
