from flask_login import current_user

from app.models.post import Post
from app.services.post import PostService
from .utils import login


def test_get_all_posts(client):
    response = client.get("posts/all", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    login(client, "test_user_1")
    response = client.get("posts/all", follow_redirects=True)
    post_service: PostService = PostService()
    posts: list[Post] = post_service.get_all()
    assert response.status_code == 200
    assert str.encode(posts[0].body) in response.data


def test_get_all_user_posts(client):
    response = client.get("posts/my_posts", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    login(client, "test_user_1")
    response = client.get("posts/my_posts", follow_redirects=True)
    post_service: PostService = PostService()
    posts: list[Post] = post_service.get_all()
    assert response.status_code == 200
    assert str.encode(posts[0].body) in response.data
    assert str.encode(posts[5].body) not in response.data


def test_get_post_by_id(client):
    response = client.get("posts/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    login(client, "test_user_1")
    response = client.get("posts/100", follow_redirects=True)
    post_service: PostService = PostService()
    post: Post = post_service.get(id=100)
    assert response.status_code == 404
    assert post is None
    response = client.get("posts/1", follow_redirects=True)
    post_service: PostService = PostService()
    post: Post = post_service.get(id=1)
    assert response.status_code == 200
    assert str.encode(post.body) in response.data
    assert str.encode(post.author.username) in response.data


def test_create_post(client):
    """Accessing crate page should be prohibited for unauthorized users"""

    response = client.get("posts/create", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    login(client, "test_user_1")
    post_data: dict = {
        "title": "unique test post title",
        "body": "unique test post body",
        "user_id": current_user.id,
    }
    response = client.get("posts/all", follow_redirects=True)
    assert str.encode(post_data["title"]) not in response.data
    assert str.encode(post_data["body"]) not in response.data

    response = client.post("posts/create", data=post_data, follow_redirects=True)
    assert response.status_code == 200
    assert str.encode(post_data["title"]) in response.data
    assert str.encode(post_data["body"]) in response.data


def test_update_post(client):
    """Accessing update page should be prohibited for unauthorized users or for anoter user's posts"""

    response = client.get("posts/1/update", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    login(client, "test_user_1")
    response = client.get("posts/5/update", follow_redirects=True)
    assert response.status_code == 405
    assert b"You&#39;re not allowed to change other user&#39;s posts" in response.data
    response = client.get("posts/100/update", follow_redirects=True)
    post_service: PostService = PostService()
    post: Post = post_service.get(id=100)
    assert response.status_code == 404
    assert post is None
    update_data: dict = {
        "title": "Unique updated title",
        "body": "Unique updated body",
    }
    response = client.get("posts/all", follow_redirects=True)
    assert str.encode(update_data["title"]) not in response.data
    assert str.encode(update_data["body"]) not in response.data
    response = client.post("posts/1/update", data=update_data, follow_redirects=True)
    assert response.status_code == 200
    assert str.encode(update_data["title"]) in response.data
    assert str.encode(update_data["body"]) in response.data


def test_delete_post(client):
    response = client.delete("posts/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    login(client, "test_user_1")
    response = client.delete("posts/5/delete", follow_redirects=True)
    assert response.status_code == 405
    assert b"You&#39;re not allowed to delete other user&#39;s posts" in response.data
    response = client.delete("posts/100/delete", follow_redirects=True)
    post_service: PostService = PostService()
    post: Post = post_service.get(id=100)
    assert response.status_code == 404
    assert post is None
    response = client.get("posts/all", follow_redirects=True)
    post_service: PostService = PostService()
    post: Post = post_service.get(id=1)
    assert str.encode(post.title) in response.data
    assert str.encode(post.body) in response.data
    response = client.delete("posts/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert str.encode(post.title) not in response.data
    assert str.encode(post.body) not in response.data
    