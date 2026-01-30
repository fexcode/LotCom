from sqlmodel import create_engine, Session, select, func
from .models import Message

engine = create_engine("sqlite:///lotcom.db")


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


def get_messages_count():
    with Session(engine) as session:
        stmt = select(func.count(1)).select_from(Message)
        result = session.exec(stmt).one()

        return result


def serialize_msg(msg:Message):
    return {
        "id": msg.id,
        "content": msg.content,
        "create_time": msg.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "sender": msg.username,
    }


create_message = create_message_by_name
