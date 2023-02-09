#!/usr/bin/env python3
"""
This module contains the class SessionAuth
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ SessionAuth class. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        from uuid import uuid4
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)
