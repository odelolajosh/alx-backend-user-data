#!/usr/bin/env python3
"""
This module contains the BasicAuth class that inherits from Auth
"""
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii
import re


class BasicAuth(Auth):
    """ BasicAuth class. """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Get the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """ Decode a Base64 string. """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            raw_header = base64.b64decode(base64_authorization_header)
            return raw_header.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """ Returns the user email and password from the
        Base64 decoded value.
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        pattern = r'([^:]+):(.+)'
        match = re.fullmatch(pattern, decoded_base64_authorization_header)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """ Returns a User object based on his email and password. """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
