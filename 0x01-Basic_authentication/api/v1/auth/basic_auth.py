#!/usr/bin/env python3
"""
This module contains the BasicAuth class that inherits from Auth
"""
from api.v1.auth.auth import Auth
import base64
import binascii


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
