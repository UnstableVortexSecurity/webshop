import pytest

from bs4 import BeautifulSoup

from utils import user_datastore
from models import db
import app


@pytest.fixture
def anonymous_client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            db.drop_all()
            db.create_all()
            yield client


@pytest.fixture
def logged_in_client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            db.drop_all()
            db.create_all()
            user = user_datastore.create_user(email="test", password="test")
            user.name = 'test'

            r = client.get('/login')

            soup = BeautifulSoup(r.data.decode(), 'html.parser')

            for input_tag in soup.find_all('input'):
                if input_tag['name'] == 'csrf_token':
                    csrf_token = input_tag['value']

            r = client.post('/login', data=dict(
                email='test',
                password='test',
                csrf_token=csrf_token
            ), follow_redirects=True)

            assert r.status_code == 200
            yield client


@pytest.fixture
def admin_client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            db.drop_all()
            db.create_all()
            user_datastore.create_role(name='administrator')
            user = user_datastore.create_user(email="test", password="test", roles=['administrator'])
            user.name = 'test'

            r = client.get('/login')

            soup = BeautifulSoup(r.data.decode(), 'html.parser')

            for input_tag in soup.find_all('input'):
                if input_tag['name'] == 'csrf_token':
                    csrf_token = input_tag['value']

            r = client.post('/login', data=dict(
                email='test',
                password='test',
                csrf_token=csrf_token
            ), follow_redirects=True)

            assert r.status_code == 200
            yield client


#
# The actual tests
#
# Syntax:
# test_{username}_{type of test}_{subject of test}(...)
# username: admin, user, anonymous


#
# Some simple ux tests first
#

def test_admin_have_admin_button_homepage(admin_client):
    r = admin_client.get('/')
    assert r.status_code == 200

    soup = BeautifulSoup(r.data.decode(), 'html.parser')

    menu_items = soup.body.nav.div.div.find_all('li')
    have_button = False
    for item in menu_items:
        if item.a.string == 'Administrate':
            have_button = True

    assert have_button


def test_user_not_have_admin_button_homepage(logged_in_client):
    r = logged_in_client.get('/')
    assert r.status_code == 200

    soup = BeautifulSoup(r.data.decode(), 'html.parser')

    menu_items = soup.body.nav.div.div.find_all('li')
    have_button = False
    for item in menu_items:
        if item.a.string == 'Administrate':
            have_button = True

    assert not have_button


def test_anonymous_not_have_admin_button_homepage(anonymous_client):
    r = anonymous_client.get('/')
    assert r.status_code == 200

    soup = BeautifulSoup(r.data.decode(), 'html.parser')

    menu_items = soup.body.nav.div.div.find_all('li')
    have_button = False
    for item in menu_items:
        if item.a.string == 'Administrate':
            have_button = True

    assert not have_button


def test_anonymous_have_to_login_protected_pages(anonymous_client):
    r = anonymous_client.get('/upload')
    assert r.status_code == 200

    soup = BeautifulSoup(r.data.decode(), 'html.parser')

    assert 'Log in' == soup.find_all('p')[0].a.string


def test_anonymous_get_login_required_redirect(anonymous_client):
    for path in ['/content/caff/1', '/profile']:
        r = anonymous_client.get(path)
        assert r.status_code == 302


def test_anonymous_post_login_required_redirect(anonymous_client):
    for path in ['/upload', '/item/1']:
        r = anonymous_client.post(path)
        assert r.status_code == 302


def test_logged_in_ok(logged_in_client):
    r = logged_in_client.get('/profile')
    assert r.status_code == 200


#
# Admin pages
#


def test_admin_access_admin(admin_client):
    for path in ['/admin/', '/admin/user/', '/admin/comment/', '/admin/item/', '/admin/purchase/']:
        r = admin_client.get(path)
        assert r.status_code == 200


def test_user_access_admin(logged_in_client):
    for path in ['/admin/', '/admin/user/', '/admin/comment/', '/admin/item/', '/admin/purchase/']:
        r = logged_in_client.get(path)
        assert r.status_code == 401


def test_anonymus_access_admin(anonymous_client):
    for path in ['/admin/', '/admin/user/', '/admin/comment/', '/admin/item/', '/admin/purchase/']:
        r = anonymous_client.get(path)
        assert r.status_code == 401
