from .base import BaseService
from app.models import User
from app.custom_types import CreateUser, PydanticUser


class UserService(BaseService):
    model = User
    create_schema = CreateUser
    get_schema = PydanticUser

    def create_user(self, schema: create_schema, **kwargs) -> User:
        """
        Creates user.

        Parameters
        ----------
            schema : CreateUser
                user data object
            kwargs : dict
                dictionary with an arbitrary number of keyword arguments

        Returns
        ----------
            User model object
        """
        return self.create(CreateUser(**schema))
