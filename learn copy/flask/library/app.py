# models.py
from typing import Any, Dict, List
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from config import db, sqlite_db_name
from routes import books_blueprint, authors_blueprint, auth_blueprint, users_blueprint
from models import Book, Author, User
from datetime import datetime
import json

import csv

def get_bootstrap_data() -> List[object]:
    bootstrap_data: List[object] = list()
    with open('flask/library/data/authors.csv', 'r') as csv_file:
        bootstrap_data.extend(Author(
            name=line["name"],
            birth_year=line["birth_year"]
        ) for line in csv.DictReader(csv_file, ["name", "birth_year"]))

    with open('flask/library/data/books.csv', 'r') as csv_file:
        bootstrap_data.extend(Book(
            series=line.get("series", ''),
            title=line.get("title"),
            published_year=int(line.get("published_year")),
            author_name=line.get("author_name")
        ) for line in csv.DictReader(csv_file, ["series", "title", "published_year", "author_name"], delimiter='|'))

    with open('flask/library/data/users.csv', 'r') as csv_file:
        bootstrap_data.extend(User(
            first_name=line["first_name"],
            last_name=line["last_name"],
            birth_date=datetime.strptime(line['birth_date'], '%Y-%m-%d').date(),
            email=line["email"]
        ) for line in csv.DictReader(csv_file, ["first_name", "last_name", "birth_date", "email"]))

    return bootstrap_data

def create_app():
    app = Flask(__name__, static_url_path='/app/v1')
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['APPLICATION_ROOT'] = '/app/v1'

    with open('flask/library/secrets.json', 'r') as json_file:
        json_data = json.loads(json_file.read())
        app.config["JWT_SECRET_KEY"] = json_data["JWT_SECRET_KEY"]

    jwt = JWTManager(app)

    db.init_app(app)

    app.register_blueprint(blueprint=books_blueprint, url_prefix='/books')
    app.register_blueprint(blueprint=authors_blueprint, url_prefix='/authors')
    app.register_blueprint(blueprint=auth_blueprint, url_prefix='/auth')
    app.register_blueprint(blueprint=users_blueprint, url_prefix='/users')

    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.add_all(get_bootstrap_data())
        db.session.commit()
    
    return app

if __name__=="__main__":
    app = create_app()
    app.run(debug=True)
