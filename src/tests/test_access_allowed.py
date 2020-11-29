import pytest

import app


@pytest.fixture
def client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        yield client


def test_login_required(client):

    r = client.get('/content/caff/1')

    assert r.status_code == 302

    # TODO Test eache endpoint with an anonymus, registered and admin user