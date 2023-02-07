#!/usr/bin/env python3
"""
This module contains the BasicAuth class that inherits from Auth
"""
from api.v1.auth.auth import Auth


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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decode a Base64 string. """
        if not self.extract_base64_authorization_header(base64_authorization_header):
            return None
        try:
            return base64_authorization_header.decode('utf-8')
        except Exception:
            return None
