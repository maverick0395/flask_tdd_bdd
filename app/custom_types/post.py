from datetime import datetime
from typing import Optional, Type

from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.models import Post


PydanticPost: Type[BaseModel] = sqlalchemy_to_pydantic(Post)


class CreatePost(BaseModel):
    """Expected data during post creation."""

    title: str
    body: str
    user_id: int
