#!/usr/bin/env python3
"""
This module contains the class SessionDBAuth
"""
from .session_exp_auth import SessionExpAuth
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth Class. """

    def create_session(self, user_id: str = None):
        """ Create a session. """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        from models.user_session import UserSession
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """ Returns a User ID based on a Session ID """
        if not session_id:
            return None
        from models.user_session import UserSession
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        if self.session_duration <= 0:
            return user_sessions[0].user_id
        duration = timedelta(seconds=self.session_duration)
        expiry_time = user_sessions[0].created_at + duration
        if expiry_time < datetime.utcnow():
            print('expired')
            user_sessions[0].remove()
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """ Deletes the user session / logout. """
        if not request:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False
        from models.user_session import UserSession
        user_sessions = UserSession.search({'session_id': session_cookie})
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
