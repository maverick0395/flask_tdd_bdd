from urllib import response
from flask_login import current_user, login_user

from app.services.post import PostService
from .utils import login, register

from app.models import Post


def test_get_all_posts(client):
    response = client.get("posts/all", follow_redirects=True)
    assert b"Please log in to access this page" in response.data
    login(client, "test_user_1")
    response = client.get("posts/all", follow_redirects=True)
    post_service: PostService = PostService()
    posts = post_service.get_all()
    assert str.encode(posts[0].body) in response.data
