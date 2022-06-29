import pytest

from .utils import populate_posts, populate_users

from app import db, create_app


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        populate_users()
        populate_posts()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop


@pytest.fixture
def test_user_register(client):
    response = client.post(
        "auth/register",
        data=dict(
            username="sam",
            email="sam@test.com",
            password="password",
            password_confirmation="password",
        ),
        follow_redirects=True,
    )
    assert response
