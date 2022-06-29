from .constants import TEST_USERS_DATA
from app.models import User
from app.services import UserService


def populate_users() -> list[User]:
    """Inserts user entities into database.

    Returns:
    --------
        list[User]:
            list of User objects
    """
    users: list[User] = []
    user_service: UserService = UserService()
    for test_user in TEST_USERS_DATA:
        user = user_service.create_user(test_user)
        users.append(user)
    return users
