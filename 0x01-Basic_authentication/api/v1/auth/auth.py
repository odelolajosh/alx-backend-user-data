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
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path[-2:] == '/*':
                excluded_path = excluded_path[:-1]
                if excluded_path == path[:len(excluded_path)]:
                    return False

            if excluded_path[-1] != '/':
                excluded_path += '/'

            if excluded_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns None - request will not contain an authorization header """
        if not request:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None - request will not contain the user information """
        return None
