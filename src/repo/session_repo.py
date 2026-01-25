from sqlmodel import create_engine, Session, select
from .models import LoginSession

engine = create_engine("sqlite:///lotcom.db")

def create_login_session(username: str, session_key: str) -> LoginSession:
    with Session(engine) as session:
        login_session = LoginSession(username=username, session_key=session_key)
        session.add(login_session)
        session.commit()
        session.refresh(login_session)
        return login_session


def get_login_session_by_key(session_key: str) -> LoginSession | None:
    with Session(engine) as session:
        stmt = select(LoginSession).where(LoginSession.session_key == session_key)
        result = session.exec(stmt).first()

        return result


def delete_login_session_by_key(session_key: str) -> None:
    with Session(engine) as session:
        stmt = select(LoginSession).where(LoginSession.session_key == session_key)
        result = session.exec(stmt).first()
        if result:
            session.delete(result)
            session.commit()


def load_sessions() -> dict[str, str]:
    with Session(engine) as session:
        stmt = select(LoginSession)
        result = session.exec(stmt).all()
        sessions = {}
        for session in result:
            sessions[session.session_key] = session.username
        return sessions
