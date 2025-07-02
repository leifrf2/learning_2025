from typing import List
from flask import Blueprint, Request, jsonify, request
from config import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api import facebook_manager
from datetime import date, datetime

"""
1. user create account
2. user login
3. user can friend another user
4. user creates a post
5. user reacts to a post
6. user replies to a post
7. user logout
"""

app_blueprint = Blueprint('auth', __name__)

# TODO - implement
def is_valid_email(email_str: str) -> bool:
    return True

# TODO - confirm input format
def parse_request_date(request_date: str) -> date:
    return datetime.strptime(request_date, "%Y-%m-%d").date()

@app_blueprint.route('/create', methods=["POST"])
def create_account():
    data = request.json

    if not is_valid_email(data.get("email", str())):
        return f"email field is not present or invalid", 401

    if facebook_manager.email_in_use(data["email"]):
        return f"email is already in use", 401

    new_user = facebook_manager.add_user(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        birth_date=parse_request_date(data["birth_date"])
    )

    return jsonify(new_user.to_dict()), 201
    

@app_blueprint.route('/login', methods=["POST"])
def user_login():
    data = request.json

    user_id = data["user_id"]

    if user_id not in facebook_manager.users.keys():
        return f"user not found", 404

    facebook_manager.current_user = facebook_manager.users[user_id]


@app_blueprint.route('/users', methods=["GET"])
def get_users():
    return jsonify([user.to_dict() for user in facebook_manager.users.values()])

