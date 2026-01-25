from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


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

class LoginSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, foreign_key="user.username")
    session_key: str = Field(max_length=50)
    create_time: datetime = Field(default_factory=datetime.now)

    # 关系定义
    user: User = Relationship(back_populates="login_sessions")