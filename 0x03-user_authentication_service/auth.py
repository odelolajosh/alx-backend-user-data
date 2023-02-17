#!/usr/bin/env python3
""" Auth. """
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hashes a password. """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generates a uuid. """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if a login is valid and successful. """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password=password.encode("utf-8"),
                hashed_password=user.hashed_password.encode("utf-8")
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Creates a new login session. """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """ Return the User corresponding to a session id. """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """ Destroys a session. """
        if user_id:
            self._db.update_user(user_id, session_id=None)
