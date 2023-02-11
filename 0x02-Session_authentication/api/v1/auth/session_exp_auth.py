#!/usr/bin/env python3
"""
This module contains the class SessionAuth
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth Class. """

    def __init__(self):
        """ Loads important instance attributes. """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None):
        """ Create a session. """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_id = self.user_id_by_session_id[session_id]
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """ Returns a User ID based on a Session ID """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        session_dict = self.user_id_by_session_id.get(session_id, None)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        duration = timedelta(seconds=self.session_duration)
        expiry_time = session_dict['created_at'] + duration
        if expiry_time < datetime.utcnow():
            del self.user_id_by_session_id[session_id]
            return None
        return session_dict['user_id']
