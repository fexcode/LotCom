import uuid
from .repo import (
    create_user,
    create_login_session,
    load_sessions,
    delete_login_session_by_key,
    get_user_by_name,
)


class LoginManager:
    def __init__(self):
        self.sessions: dict[str, str] = load_sessions()
        print("加载了sessions: ", self.sessions)

    def signup(self, username, password, studentid):
        if not self.user_exists(username):
            create_user(username=username, password=password, student_id=studentid)
        else:
            raise ValueError("Username already exists")

    def user_exists(self, username):
        return get_user_by_name(username=username) is not None

    def _verify_user(self, username, password):
        user = get_user_by_name(username=username)
        if user is not None and user.password == password:
            return True
        else:
            return False

    def login(self, username, password):
        if self._verify_user(username, password):
            session_id = uuid.uuid4().hex
            self.sessions[session_id] = username
            create_login_session(username=username, session_key=session_id)
            return session_id
        else:
            return None

    def logout(self, session_id):
        if session_id in self.sessions:
            delete_login_session_by_key(session_key=session_id)
            del self.sessions[session_id]

    def get_username(self, session_id):
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            return None

    def is_logged_in(self, session_id):
        return session_id in self.sessions
