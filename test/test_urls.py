from flask import url_for
from hello import app


def test_urls():
    with app.test_request_context():
        assert url_for('index') == '/'
        assert url_for('hello') == '/hello'
        assert url_for('user', username='Manu') == '/hello/Manu'
