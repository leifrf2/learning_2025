from typing import Any, Dict, List
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, date
from routes import answers_blueprint, question_blueprint, auth_blueprint
from config import db, sqlite_db_name
import json
import csv


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "rippling_interview"

    jwt = JWTManager(app)
    db.init_app(app)

    app.register_blueprint(blueprint=question_blueprint, url_prefix='/questions')
    app.register_blueprint(blueprint=answers_blueprint, url_prefix='/answers')
    app.register_blueprint(blueprint=auth_blueprint, url_prefix='/auth')

    with app.app_context():
        db.drop_all()
        db.create_all()
    
    return app

if __name__=="__main__":
    app = create_app()
    app.run(debug=True)
