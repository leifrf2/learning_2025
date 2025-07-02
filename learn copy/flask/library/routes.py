from flask import Blueprint, jsonify, request
from models import Book, Author, User
from config import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from typing import Dict, List, Set
from datetime import datetime, date
from dataclasses import dataclass
from itertools import groupby

##### books #####

@dataclass
class Series:
    title: str
    num_books: int
    first_published_year: int
    last_published_year: int
    author_names: Set[str]

    def to_dict(self):
        return {
            "title": self.title,
            "num_books" : self.num_books,
            "first_published_year" : self.first_published_year,
            "last_published_year" : self.last_published_year,
            "author_names": list(self.author_names)
        }

books_blueprint = Blueprint('books', __name__)

@books_blueprint.route(rule='',methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

@books_blueprint.route(rule='/series',methods=['GET'])
def get_series():
    books: List[Book] = Book.query.all()

    book_groups = (list(g) for _, g in groupby(books, key=lambda x: x.series))

    series = sorted((Series(
        title=g[0].series,
        num_books=len(g),
        first_published_year=min((b.published_year for b in g)),
        last_published_year=max((b.published_year for b in g)),
        author_names={b.author.name for b in g}
        ) for g in book_groups if len(g) > 1), key=lambda x: x.num_books, reverse=True)
    
    return jsonify([series_object.to_dict() for series_object in series]), 200

@books_blueprint.route(rule="/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict()), 200

@books_blueprint.route(rule=f'/count', methods=['GET'])
def get_books_count():
    return jsonify(Book.query.count()), 200

@books_blueprint.route(rule='', methods=['POST'])
def create_book():
    data = request.json
    book = Book(
        title=data["Title"],
        author_name=data["Author"],
        published_year=int(data["Published Year"]),
        series=data.get("Series", '')
    )
    db.session.add(book)

    author_name = data["Author"]
    authors: List[Author] = Author.query.filter_by(name=author_name).all()
    if len(authors) == 0:
        # this author doesn't exist yet, create it
        db.session.add(Author(
            birth_year=None,
            name=author_name
        ))

    db.session.commit()

    return jsonify(book.to_dict()), 201

@books_blueprint.route(rule='/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book: Book = Book.query.get_or_404(book_id)
    
    if "Title" in data:
        book.title = data.get("Title")
    if "Author" in data:
        book.author = data.get("Author")
    if "Published Year" in data:
        book.published_year = data.get("Published Year")
    if "Series" in data:
        book.series = data.get("Series")
    
    db.session.commit()

    return jsonify(book.to_dict()), 200

@books_blueprint.route(rule='/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book: Book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return '', 204

##### authors #####

authors_blueprint = Blueprint('authors', __name__)

@authors_blueprint.route(rule='',methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([author.to_dict() for author in authors]), 200

@authors_blueprint.route(rule="/<int:author_id>", methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id)

    data: Dict = request.get_json()

    return_dict = author.to_dict()

    if "include_books" in data.keys() and data["include_books"] == True:
        return_dict['books'] = [
            book.to_dict() for book in author.books
        ]

    return jsonify(return_dict), 200

@authors_blueprint.route(rule=f'/count', methods=['GET'])
def get_authors_count():
    return jsonify(Author.query.count()), 200

@authors_blueprint.route(rule='', methods=['POST'])
def create_author():
    data = request.json
    author = Author(
        name=data["name"],
        birth_year=data["birth_year"]
    )

    db.session.add(author)
    db.session.commit()

    return jsonify(author.to_dict()), 201

@authors_blueprint.route(rule='/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    data = request.json
    author: Author = Author.query.get_or_404(author_id)
    
    if "name" in data:
        author.name = data.get("name")
    if "birth_year" in data:
        author.birth_year = data.get("birth_year")
    
    db.session.commit()

    return jsonify(author.to_dict()), 200

@authors_blueprint.route(rule='/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    author: Author = Author.query.get_or_404(author_id)

    db.session.delete(author)
    db.session.commit()

    return '', 204

##### users #####

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    return jsonify(user.to_dict()), 200

##### auth #####

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data: Dict = request.get_json()

    required_fields = [
        "first_name",
        "last_name",
        "birth_date",
        "email"
    ]

    for field in required_fields:
        if field not in data.keys():
            return f"missing required field: {field}", 400

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date(),
        email=data["email"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "createdAt": user.created_at.isoformat() + "Z"
    }), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if "user_id" not in data.keys():
        return f"Missing required field: user_id", 400
    
    user_id = data["user_id"]

    user = User.query.get_or_404(user_id)

    access_token = create_access_token(user.id)

    return jsonify({
        "id": user.id,
        "access_token": access_token
    }), 200

