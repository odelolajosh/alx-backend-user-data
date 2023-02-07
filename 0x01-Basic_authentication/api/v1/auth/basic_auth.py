#!/usr/bin/env python3
"""
This module contains the BasicAuth class that inherits from Auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class. """
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Get the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if not self.authorization_header(authorization_header):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]
