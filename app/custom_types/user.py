from datetime import datetime
from typing import Optional, Type

from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.models import User

PydanticUser: Type[BaseModel] = sqlalchemy_to_pydantic(User)


class CreateUser(BaseModel):
    """Expected data during post creation."""

    username: str
    email: str
    password: str
