from typing import Any, Dict, Optional
from sqlalchemy import Date, DateTime, ForeignKey, Column, Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from datetime import datetime, timezone

# Question

class Question(db.Model):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, nullable=False)
    created_datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    content = Column(Text, nullable=False)
    answers = db.relationship("Answer", back_populates="question")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = db.relationship("User", back_populates="questions")

    def __init__(self, content: str, user_id: int):
        self.content = content
        self.user_id = user_id

    def to_dict(self):
        return {
            "id" : self.id,
            "user_id": self.user_id,
            "content" : self.content,
            "created_datetime" : self.created_datetime,
            "updated_datetime" : self.updated_datetime
        }


# Answer

class Answer(db.Model):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    upvote_count = Column(Integer, nullable=False, default=0)
    view_count = Column(Integer, nullable=False, default=0)

    question_id = Column(Integer, ForeignKey(column="questions.id"), nullable=False)
    question = db.relationship("Question", back_populates="answers")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="answers")

    def __init__(self, content: str, question_id: int, user_id: int):
        self.content = content
        self.question_id = question_id
        self.user_id = user_id


    def to_dict(self) -> Dict:
        return {
            "id" : self.id,
            "content" : self.content,
            "created_datetime" : self.created_datetime,
            "updated_datetime" : self.updated_datetime,
            "upvote_count" : self.upvote_count,
            "view_count" : self.view_count,
            "question_id" : self.question_id,
            "user_id" : self.user_id
        }


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    created_datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_datetime = Column(DateTime, nullable=False, default=datetime.utcnow())

    questions = db.relationship("Question", back_populates="user")
    answers = db.relationship("Answer", back_populates="user")

    def __init__(self,
                 first_name,
                 last_name,
                 birth_date,
                 email,
                 hashed_password):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date # formatting
        self.email = email
        self.password_hash = hashed_password

    def to_dict(self):
        return {
            "id" : self.id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "created_datetime" : self.created_datetime,
            "updated_datetime" : self.updated_datetime,
            "email" : self.email,
            "birth_date" : self.birth_date
        }