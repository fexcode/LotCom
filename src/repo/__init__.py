from sqlmodel import SQLModel, create_engine
from .user_repo import create_engine, create_user, get_user_by_name
from .message_repo import (
    get_all_messages,
    create_message_by_name,
    get_messages_count,
    create_message,
)
from .session_repo import (
    create_login_session,
    get_login_session_by_key,
    delete_login_session_by_key,
    load_sessions,
)
from .models import User, Message, LoginSession


engine = create_engine("sqlite:///lotcom.db")

SQLModel.metadata.create_all(engine)

__all__ = [
    "User",
    "Message",
    "LoginSession",
    "create_engine",
    "create_user",
    "get_user_by_name",
    "get_all_messages",
    "create_message_by_name",
    "get_messages_count",
    "create_message",
    "create_login_session",
    "get_login_session_by_key",
    "delete_login_session_by_key",
    "load_sessions",
]
