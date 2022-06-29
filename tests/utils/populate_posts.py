from .constants import TEST_POSTS_DATA
from app.models import Post
from app.services import PostService


def populate_posts() -> list[Post]:
    """Inserts post entities into database.

    Returns:
    --------
        list[Post]:
            list of Post objects
    """
    posts: list[Post] = []
    post_service: PostService = PostService()
    for test_post in TEST_POSTS_DATA:
        post = post_service.create_post(test_post)
        posts.append(post)
    return posts
