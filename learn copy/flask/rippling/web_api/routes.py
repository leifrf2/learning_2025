from typing import Dict
from flask import Blueprint, jsonify, request
from config import db
from models import Question, Answer, User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# helpers

def get_active_user_id() -> int:
    return get_jwt_identity()

# Question

question_blueprint = Blueprint('questions', __name__)


@question_blueprint.route('', methods=["POST"])
@jwt_required() # user login required
def create_question():
    data: Dict = request.json
    content_field_name = "content"

    if content_field_name in data.keys():
        content = data[content_field_name]
        current_user_id = get_active_user_id()

        new_question = Question(
            content=content,
            user_id=current_user_id
        )

        db.session.add(new_question)
        db.session.commit()

        return jsonify(new_question.to_dict()), 201

    else:
        return f"content missing from request", 400


@question_blueprint.route('/<int:question_id>', methods=["POST"])
@jwt_required() # user login required
def update_question(question_id: int):
    data: Dict = request.json
    content_field_name = "content"

    question: Question = Question.query.get_or_404(question_id)

    if question.user_id != get_active_user_id():
        return "user must be author of this question to update it", 401

    if content_field_name in data.keys():
        content = data[content_field_name]

        question.content = content
        question.updated_datetime = datetime.utcnow()

        db.session.add(question)
        db.session.commit()

        return jsonify(question.to_dict()), 200

    else:
        return f"content missing from request", 400


@question_blueprint.route('/<int:question_id>', methods=["GET"])
def get_question(question_id: int):
    question: Question = Question.query.get_or_404(question_id)
    return jsonify(question.to_dict()), 200


@question_blueprint.route('/<int:question_id>/related', methods=["GET"])
def get_related_questions(question_id: int):
    # sort logic?
    # count?
    raise NotImplementedError(f"this will be a service call to get the related questions based on some scoring logic")


@question_blueprint.route('/<int:question_id>/answers', methods=["GET"])
def get_related_answers(question_id: int):
    # sort logic?
    # count?
    # TODO
    pass

# Answer

answers_blueprint = Blueprint('answers', __name__)


@answers_blueprint.route('', methods=["POST"])
@jwt_required()
def create_answer():
    data: Dict = request.json
    question_id_key = "question_id"
    content_key = "content"    

    if all(key in data.keys() for key in [question_id_key, content_key]):
        return f"body must include fields: {[question_id_key, content_key]}", 400

    new_answer: Answer = Answer(
        content=data[content_key],
        question_id=data[question_id_key],
        user_id=get_active_user_id()
    )

    db.session.add(new_answer)
    db.session.commit()

    return jsonify(new_answer.to_dict()), 201


@answers_blueprint.route('/<int:answer_id>', methods=["POST"])
@jwt_required()
def update_answer(answer_id: int):
    data: Dict = request.json
    content_key = "content"
    current_user_id = get_active_user_id()

    answer: Answer = Answer.query.get_or_404(answer_id)

    if answer.user_id != current_user_id:
        return f"user must be author of the answer to update it", 401

    if content_key not in data.keys():
        return f"no content found in the body of the request", 400
    
    answer.content = data[content_key]

    db.session.add(answer)
    db.session.commit()

    return jsonify(answer), 200


@answers_blueprint.route('/<int:answer_id>', methods=["GET"])
def get_answer(answer_id: int):
    answer: Answer = Answer.query.get_or_404(answer_id)

    return jsonify(answer), 200


@answers_blueprint.route('/<int:answer_id>/upvote', methods=["POST"])
@jwt_required()
def upvote_answer(answer_id: int):
    current_user_id = get_active_user_id()

    answer: Answer = Answer.query.get_or_404(answer_id)
    
    # if user has not alread upvoted this answer
    # upvote it

    answer.upvote_count += 1

    # update upvotes table

    db.session.add(answer)
    db.session.commit()

    return jsonify(answer), 200


@answers_blueprint.route('/<int:answer_id>/remove_upvote', methods=["POST"])
@jwt_required()
def remove_upvote_answer(answer_id: int):
    current_user_id = get_active_user_id()

    answer: Answer = Answer.query.get_or_404(answer_id)
    
    # if user has  already upvoted this answer
    # remove it

    answer.upvote_count -= 1

    # update upvotes table

    db.session.add(answer)
    db.session.commit()

    return jsonify(answer), 200
    

# : get_comments(id, count) # always chronological

# Auth

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route('/register', methods=["POST"])
def register():
    data: Dict = request.json
    birthdate_field = "birth_date"
    firstname_field = "first_name"
    lastname_field = "last_name"
    email_field = "email"
    password_field = "password"
    required_fields = [birthdate_field, firstname_field, lastname_field, email_field, password_field]

    if any(field not in data.keys() for field in required_fields):
        return f"missing one of required fields: {required_fields}", 400

    new_user = User(
        birth_date= datetime.strptime(data[birthdate_field], "%Y-%m-%d").date(),
        first_name=data[firstname_field],
        last_name=data[lastname_field],
        email=data[email_field],
        hashed_password=generate_password_hash(data[password_field], method="pbkdf2")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


@auth_blueprint.route('/login', methods=["POST"])
def login():
    data: Dict = request.json
    email_field = "email"
    password_field = "password"
    required_fields = [email_field, password_field]

    if any(field not in data.keys() for field in required_fields):
        return f"missing required field in {required_fields}", 400

    user: User = User.query.filter_by(email=data[email_field]).first_or_404()

    if check_password_hash(user.password_hash, data[password_field]):
        response_dict = user.to_dict()
        response_dict["token"] = create_access_token(identity=user.id)
        return jsonify(response_dict), 200