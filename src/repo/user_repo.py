from sqlmodel import create_engine, Session, select
from .models import User

engine = create_engine("sqlite:///lotcom.db")

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
