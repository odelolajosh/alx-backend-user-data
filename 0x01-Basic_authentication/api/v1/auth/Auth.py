#!/usr/bin/env python3
"""
This module contains the Auth class
- that manages the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to interact with the authentication database """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False - path will not be excluded """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns None - request will not contain an authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None - request will not contain the user information """
        return None
