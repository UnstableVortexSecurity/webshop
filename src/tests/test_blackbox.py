import pytest

from bs4 import BeautifulSoup

from flask import Response
from utils import user_datastore
from models import db, Item, Purchase
import app


def create_db_setup():
    db.drop_all()
    db.create_all()
    user_datastore.create_role(name='administrator')
    admin_user = user_datastore.create_user(email="admin", password="admin", roles=['administrator'])
    other_user = user_datastore.create_user(email="user", password="user")
    admin_user.name = 'admin'
    other_user.name = 'user'

    item_a = Item(name="a", uploader=admin_user)
    item_b = Item(name="b", uploader=admin_user)
    item_c = Item(name="c", uploader=other_user)
    purchase = Purchase(item=item_a, purchaser=other_user)

    db.session.add(item_a)
    db.session.add(item_b)
    db.session.add(item_c)
    db.session.add(purchase)

    db.session.commit()


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
            create_db_setup()
            r = client.get('/login')

            soup = BeautifulSoup(r.data.decode(), 'html.parser')

            for input_tag in soup.find_all('input'):
                if input_tag['name'] == 'csrf_token':
                    csrf_token = input_tag['value']

            r = client.post('/login', data=dict(
                email='user',
                password='user',
                csrf_token=csrf_token
            ), follow_redirects=True)

            assert r.status_code == 200
            yield client


@pytest.fixture
def admin_client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            create_db_setup()

            r = client.get('/login')

            soup = BeautifulSoup(r.data.decode(), 'html.parser')

            for input_tag in soup.find_all('input'):
                if input_tag['name'] == 'csrf_token':
                    csrf_token = input_tag['value']

            r = client.post('/login', data=dict(
                email='admin',
                password='admin',
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


#
# Some status code based tests
#


def test_anonymous_get_login_required_redirect(anonymous_client):
    for path in ['/content/caff/1', '/profile']:
        r = anonymous_client.get(path)
        assert r.status_code == 302


def test_anonymous_post_login_required_redirect(anonymous_client):
    for path in ['/upload', '/item/1']:
        r = anonymous_client.post(path)
        assert r.status_code == 302


def test_user_profile_ok(logged_in_client):
    r = logged_in_client.get('/profile')
    assert r.status_code == 200

#
# Content stuff
#

def test_user_content_nonexistent(logged_in_client):
    r = logged_in_client.get('/content/caff/4')  # nonexistant
    assert r.status_code == 404


def test_user_content_uploaded(logged_in_client, mocker):
    mocker.patch(
        'views.contentview.ContentView._stream_from_minio',
        side_effect=lambda bucket, id, fname: Response(status=200)
    )

    r = logged_in_client.get('/content/caff/3')  # existant, uploaded
    assert r.status_code == 200


def test_user_content_unpurchased(logged_in_client):
    r = logged_in_client.get('/content/caff/2')  # existant, unpurchased
    assert r.status_code == 403


def test_user_content_purchased(logged_in_client, mocker):
    mocker.patch(
        'views.contentview.ContentView._stream_from_minio',
        side_effect=lambda bucket, id, fname: Response(status=200)
    )

    r = logged_in_client.get('/content/caff/1')  # purchased
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
