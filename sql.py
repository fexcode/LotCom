from sqlmodel import SQLModel, create_engine, Session, Field, select, Relationship, func
from datetime import datetime
from typing import Optional

engine = create_engine("sqlite:///lotcom.db")


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, max_length=50)  # 学号作为主键
    student_id: int = Field(nullable=False)
    password: str = Field(max_length=50, nullable=False)

    # 关系定义
    messages: list["Message"] = Relationship(back_populates="sender")
    login_sessions: list["LoginSession"] = Relationship(back_populates="user")


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(max_length=200)
    create_time: datetime = Field(default_factory=datetime.now)

    # 添加外键字段
    username: str = Field(foreign_key="user.username", max_length=50)

    # 关系定义
    sender: User = Relationship(back_populates="messages")

    def tostr(self):
        return f"{self.username}: {self.content}"


def create_user(username: str, password: str, student_id: int) -> User:
    user = User(student_id=student_id, username=username, password=password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_by_name(username: str) -> User | None:
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        result = session.exec(stmt).first()

        return result


def get_all_messages() -> list[Message]:
    with Session(engine) as session:
        stmt = select(Message)
        result = session.exec(stmt).all()

        return list(result)


def create_message_by_name(content: str, username: str) -> Message:
    with Session(engine) as session:
        message = Message(content=content, username=username)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message


create_message = create_message_by_name


def get_messages_count():
    with Session(engine) as session:
        stmt = select(func.count(1)).select_from(Message)
        result = session.exec(stmt).one()

        return result


# ================================
class LoginSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, foreign_key="user.username")
    session_key: str = Field(max_length=50)
    create_time: datetime = Field(default_factory=datetime.now)

    # 关系定义
    user: User = Relationship(back_populates="login_sessions")


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


SQLModel.metadata.create_all(engine)
