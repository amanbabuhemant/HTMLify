from typing import Optional

from app.models import User


class UserService:

    @staticmethod
    def get_user(username: str) -> Optional[User]:
        user = User.by_username(username)
        return user

    @staticmethod
    def get_user_by_id(id: int) -> Optional[User]:
        user = User.by_id(id)
        return user

    @staticmethod
    def get_user_by_api_key(api_key: str) -> Optional[User]:
        user = User.by_api_key(api_key)
        return user

    @staticmethod
    def auth_user(user_or_username: str | User, password: str) -> bool:
        user = None
        if isinstance(user_or_username, User):
            user = user_or_username
        if isinstance(user_or_username, str):
            user = User.by_username(user_or_username)

        if not user:
            return False

        return user.match_password(password)

