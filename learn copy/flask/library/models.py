from typing import Any, Dict, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Column, Integer, String
from config import db
from datetime import datetime, timezone

class Book(db.Model):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    series = Column(String(100), nullable=True)
    published_year = Column(Integer, nullable=True)
    author_name = Column(Integer, ForeignKey('authors.name'), nullable = False)
    author = db.relationship("Author", back_populates="books")

    def __init__(self,
                 title: str,
                 series: str,
                 published_year: int,
                 author_name: str):
        self.title = title
        self.series = series
        self.published_year = published_year
        self.author_name = author_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title' : self.title,
            'series' : self.series,
            'published_year' : self.published_year,
            'author' : self.author.to_dict() if self.author else {}
        }

class Author(db.Model):
    __tablename__ = "authors"

    #id = Column(Integer, autoincrement=True, nullable=False, default=0)
    name = Column(String(100), primary_key=True)
    birth_year = Column(Integer, nullable=True)
    books = db.relationship("Book", back_populates="author")

    def __init__(self,
                 name: str,
                 birth_year: Optional[int] = None):
        self.name = name
        self.birth_year =  birth_year

    def to_dict(self) -> Dict[str, Any]:
        return {
            #'id' : self.id,
            'name': self.name,
            'birth_year' : self.birth_year
        }

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "birth_date" : self.birth_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

