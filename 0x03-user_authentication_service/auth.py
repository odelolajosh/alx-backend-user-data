#!/usr/bin/env python3
""" Auth. """
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hashes a password. """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        if not email or not password:
            return None
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            pass
        except InvalidRequestError:
            return None

        hashed_pwd = _hash_password(password).decode("utf-8")
        user = self._db.add_user(email, hashed_pwd)
        return user
