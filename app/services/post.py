from .base import BaseService
from app.models import Post
from app.custom_types import CreatePost, PydanticPost


class PostService(BaseService):
    model = Post
    create_schema = CreatePost
    get_schema = PydanticPost

    def create_post(self, schema: create_schema, **kwargs) -> Post:
        """
        Creates post.

        Parameters
        ----------
            schema : CreatePost
                post data object
            kwargs : dict
                dictionary with an arbitrary number of keyword arguments

        Returns
        ----------
            Post model object
        """
        return self.create(CreatePost(**schema))

    def update_post(self, id: int, **data) -> None:
        """
        Updates post.

        Parameters
        ----------
            id : int
                post id
            data : dict
                dictionary with an arbitrary number of keyword arguments
        """
        return self.update(id, **data)
