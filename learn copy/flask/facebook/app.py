# app.py
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import enum
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///facebook.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret')  # Change in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# ---------------------------
# DATA MODELS
# ---------------------------

# User Friendship Association Table
friendships = db.Table(
    'friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.String(500))
    location = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    sent_friend_requests = db.relationship('FriendRequest', 
                                          foreign_keys='FriendRequest.from_user_id',
                                          backref='sender', lazy=True)
    received_friend_requests = db.relationship('FriendRequest', 
                                              foreign_keys='FriendRequest.to_user_id',
                                              backref='receiver', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    friends = db.relationship('User', 
                             secondary=friendships,
                             primaryjoin=(friendships.c.user_id == id),
                             secondaryjoin=(friendships.c.friend_id == id),
                             backref=db.backref('friended_by', lazy='dynamic'),
                             lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_friend(self, user):
        if not self.is_friend(user):
            self.friends.append(user)
            user.friends.append(self)
            return self
    
    def remove_friend(self, user):
        if self.is_friend(user):
            self.friends.remove(user)
            user.friends.remove(self)
            return self
    
    def is_friend(self, user):
        return self.friends.filter(friendships.c.friend_id == user.id).count() > 0

class PrivacyType(enum.Enum):
    PUBLIC = "PUBLIC"
    FRIENDS = "FRIENDS"
    ONLY_ME = "ONLY_ME"

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    privacy = db.Column(db.Enum(PrivacyType), default=PrivacyType.PUBLIC)
    location_name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    reactions = db.relationship('Reaction', backref='post', lazy=True, 
                               primaryjoin="and_(Post.id==Reaction.content_id, "
                                          "Reaction.content_type=='POST')",
                               cascade='all, delete-orphan')
    media = db.relationship('Media', backref='post', lazy=True, 
                           primaryjoin="and_(Post.id==Media.content_id, "
                                      "Media.content_type=='POST')",
                           cascade='all, delete-orphan')

class Media(db.Model):
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'POST' or 'COMMENT'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reactions = db.relationship('Reaction', backref='comment', lazy=True,
                               primaryjoin="and_(Comment.id==Reaction.content_id, "
                                          "Reaction.content_type=='COMMENT')",
                               cascade='all, delete-orphan')
    media = db.relationship('Media', backref='comment', lazy=True,
                           primaryjoin="and_(Comment.id==Media.content_id, "
                                      "Media.content_type=='COMMENT')")

class ReactionType(enum.Enum):
    LIKE = "LIKE"
    LOVE = "LOVE"
    HAHA = "HAHA"
    WOW = "WOW"
    SAD = "SAD"
    ANGRY = "ANGRY"

class Reaction(db.Model):
    __tablename__ = 'reactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'POST' or 'COMMENT'
    reaction_type = db.Column(db.Enum(ReactionType), default=ReactionType.LIKE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='reactions')

class FriendRequestStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(FriendRequestStatus), default=FriendRequestStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NotificationType(enum.Enum):
    FRIEND_REQUEST = "FRIEND_REQUEST"
    FRIEND_ACCEPT = "FRIEND_ACCEPT"
    POST_LIKE = "POST_LIKE"
    POST_COMMENT = "POST_COMMENT"
    COMMENT_LIKE = "COMMENT_LIKE"
    COMMENT_REPLY = "COMMENT_REPLY"

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.Enum(NotificationType), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'POST', 'COMMENT', 'FRIEND_REQUEST'
    content_preview = db.Column(db.String(100))
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    actor = db.relationship('User', foreign_keys=[actor_id], backref='notifications_as_actor')

# ---------------------------
# ERROR HANDLING
# ---------------------------

class APIError(Exception):
    def __init__(self, code, message, status_code=400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        "error": {
            "code": error.code,
            "message": error.message,
            "details": error.details
        }
    }
    return jsonify(response), error.status_code

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": {
            "code": "RESOURCE_NOT_FOUND",
            "message": "The requested resource could not be found",
            "details": {}
        }
    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "details": {}
        }
    }), 500

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        raise APIError("UNAUTHORIZED", "User not found", 401)
    return user

def create_notification(user_id, actor_id, notification_type, content_id, content_type, content_preview=None):
    notification = Notification(
        user_id=user_id,
        actor_id=actor_id,
        notification_type=notification_type,
        content_id=content_id,
        content_type=content_type,
        content_preview=content_preview
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def user_to_dict(user, include_email=False):
    result = {
        "id": user.id,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "profilePicture": user.profile_picture,
        "bio": user.bio,
        "location": user.location,
        "createdAt": user.created_at.isoformat() + "Z"
    }
    
    if include_email:
        result["email"] = user.email
        
    return result

def post_to_dict(post, include_user=True):
    result = {
        "id": post.id,
        "content": post.content,
        "privacy": post.privacy.value,
        "createdAt": post.created_at.isoformat() + "Z",
        "updatedAt": post.updated_at.isoformat() + "Z"
    }
    
    if post.location_name:
        result["location"] = {
            "name": post.location_name,
            "latitude": post.latitude,
            "longitude": post.longitude
        }
    
    # Add media URLs
    media_urls = [media.url for media in post.media]
    if media_urls:
        result["mediaUrls"] = media_urls
    
    # Add counts
    result["likeCount"] = Reaction.query.filter_by(
        content_id=post.id, content_type="POST").count()
    result["commentCount"] = Comment.query.filter_by(post_id=post.id).count()
    
    # Add user info if requested
    if include_user:
        result["userId"] = post.user_id
        result["userFirstName"] = post.author.first_name
        result["userLastName"] = post.author.last_name
        result["userProfilePicture"] = post.author.profile_picture
    
    return result

def comment_to_dict(comment, include_user=True):
    result = {
        "id": comment.id,
        "postId": comment.post_id,
        "content": comment.content,
        "createdAt": comment.created_at.isoformat() + "Z",
        "updatedAt": comment.updated_at.isoformat() + "Z"
    }
    
    # Add media URL if exists
    media = Media.query.filter_by(content_id=comment.id, content_type="COMMENT").first()
    if media:
        result["mediaUrl"] = media.url
    
    # Add like count
    result["likeCount"] = Reaction.query.filter_by(
        content_id=comment.id, content_type="COMMENT").count()
    
    # Add user info if requested
    if include_user:
        result["userId"] = comment.user_id
        result["userFirstName"] = comment.author.first_name
        result["userLastName"] = comment.author.last_name
        result["userProfilePicture"] = comment.author.profile_picture
    
    return result

def reaction_to_dict(reaction, include_user=True):
    result = {
        "id": reaction.id,
        "contentId": reaction.content_id,
        "contentType": reaction.content_type,
        "reactionType": reaction.reaction_type.value,
        "createdAt": reaction.created_at.isoformat() + "Z"
    }
    
    # Add user info if requested
    if include_user:
        result["userId"] = reaction.user_id
        result["userFirstName"] = reaction.user.first_name
        result["userLastName"] = reaction.user.last_name
        result["userProfilePicture"] = reaction.user.profile_picture
    
    return result

def friend_request_to_dict(friend_request, include_users=True):
    result = {
        "id": friend_request.id,
        "status": friend_request.status.value,
        "createdAt": friend_request.created_at.isoformat() + "Z",
        "updatedAt": friend_request.updated_at.isoformat() + "Z"
    }
    
    # Add user info if requested
    if include_users:
        result["fromUserId"] = friend_request.from_user_id
        result["fromUserFirstName"] = friend_request.sender.first_name
        result["fromUserLastName"] = friend_request.sender.last_name
        result["fromUserProfilePicture"] = friend_request.sender.profile_picture
        
        result["toUserId"] = friend_request.to_user_id
        result["toUserFirstName"] = friend_request.receiver.first_name
        result["toUserLastName"] = friend_request.receiver.last_name
        result["toUserProfilePicture"] = friend_request.receiver.profile_picture
    
    return result

def notification_to_dict(notification):
    result = {
        "id": notification.id,
        "type": notification.notification_type.value,
        "contentId": notification.content_id,
        "contentType": notification.content_type,
        "read": notification.read,
        "createdAt": notification.created_at.isoformat() + "Z"
    }
    
    # Add actor info
    result["actorId"] = notification.actor_id
    result["actorName"] = f"{notification.actor.first_name} {notification.actor.last_name}"
    result["actorProfilePicture"] = notification.actor.profile_picture
    
    # Add content preview if available
    if notification.content_preview:
        result["contentPreview"] = notification.content_preview
    
    return result

# ---------------------------
# API ROUTES
# ---------------------------

# Authentication routes
@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['email', 'password', 'firstName', 'lastName', 'dateOfBirth']
    for field in required_fields:
        if field not in data:
            raise APIError("VALIDATION_ERROR", f"Missing required field: {field}")
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        raise APIError("VALIDATION_ERROR", "Email already registered", 400)
    
    # Create new user
    user = User(
        email=data['email'],
        first_name=data['firstName'],
        last_name=data['lastName'],
        date_of_birth=datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "createdAt": user.created_at.isoformat() + "Z",
        "accessToken": access_token
    }), 201

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check if required fields are present
    if 'email' not in data or 'password' not in data:
        raise APIError("VALIDATION_ERROR", "Email and password are required")
    
    # Find user
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        raise APIError("UNAUTHORIZED", "Invalid email or password", 401)
    
    # Check if user is active
    if not user.is_active:
        raise APIError("UNAUTHORIZED", "Account is deactivated", 401)
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "accessToken": access_token
    }), 200

# User routes
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    
    result = user_to_dict(user)
    
    # Add friend count
    result["friendCount"] = user.friends.count()
    
    # Check if current user is friends with this user
    current_user = get_current_user()
    result["isFriend"] = current_user.is_friend(user) if current_user.id != user_id else None
    
    return jsonify(result), 200

@app.route('/api/v1/users/me', methods=['GET'])
@jwt_required()
def get_current_user_profile():
    user = get_current_user()
    
    result = user_to_dict(user, include_email=True)
    result["friendCount"] = user.friends.count()
    
    return jsonify(result), 200

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_current_user()
    
    # Only allow users to update their own profile
    if current_user.id != user_id:
        raise APIError("FORBIDDEN", "You can only update your own profile", 403)
    
    data = request.get_json()
    allowed_fields = ['firstName', 'lastName', 'bio', 'location', 'profilePicture']
    
    # Update allowed fields
    for field in allowed_fields:
        if field in data:
            snake_case_field = ''.join(['_' + c.lower() if c.isupper() else c for c in field]).lstrip('_')
            setattr(current_user, snake_case_field, data[field])
    
    db.session.commit()
    
    return jsonify(user_to_dict(current_user, include_email=True)), 200

@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_current_user()
    
    # Only allow users to delete their own account
    if current_user.id != user_id:
        raise APIError("FORBIDDEN", "You can only delete your own account", 403)
    
    # Soft delete - mark as inactive
    current_user.is_active = False
    db.session.commit()
    
    return "", 204

# Post routes
@app.route('/api/v1/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user = get_current_user()
    data = request.get_json()
    
    # Check if required fields are present
    if 'content' not in data:
        raise APIError("VALIDATION_ERROR", "Content is required")
    
    # Create post
    post = Post(
        user_id=current_user.id,
        content=data['content'],
        privacy=PrivacyType[data.get('privacy', 'PUBLIC')]
    )
    
    # Add location if provided
    if 'location' in data:
        post.location_name = data['location'].get('name')
        post.latitude = data['location'].get('latitude')
        post.longitude = data['location'].get('longitude')
    
    db.session.add(post)
    db.session.commit()
    
    # Add media if provided
    if 'mediaUrls' in data and isinstance(data['mediaUrls'], list):
        for url in data['mediaUrls']:
            media = Media(
                url=url,
                content_id=post.id,
                content_type='POST'
            )
            db.session.add(media)
        
        db.session.commit()
    
    return jsonify(post_to_dict(post)), 201

@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = get_current_user()
    
    # Check if user can view this post
    if post.privacy == PrivacyType.ONLY_ME and post.user_id != current_user.id:
        raise APIError("FORBIDDEN", "You don't have permission to view this post", 403)
    
    if post.privacy == PrivacyType.FRIENDS and post.user_id != current_user.id:
        if not current_user.is_friend(post.author):
            raise APIError("FORBIDDEN", "You don't have permission to view this post", 403)
    
    return jsonify(post_to_dict(post)), 200

@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = get_current_user()
    
    # Only allow author to update post
    if post.user_id != current_user.id:
        raise APIError("FORBIDDEN", "You can only update your own posts", 403)
    
    data = request.get_json()
    allowed_fields = ['content', 'privacy']
    
    # Update allowed fields
    for field in allowed_fields:
        if field in data:
            if field == 'privacy':
                post.privacy = PrivacyType[data[field]]
            else:
                setattr(post, field, data[field])
    
    db.session.commit()
    
    return jsonify(post_to_dict(post, include_user=False)), 200

@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = get_current_user()
    
    # Only allow author to delete post
    if post.user_id != current_user.id:
        raise APIError("FORBIDDEN", "You can only delete your own posts", 403)
    
    db.session.delete(post)
    db.session.commit()
    
    return "", 204

@app.route('/api/v1/feed', methods=['GET'])
@jwt_required()
def get_feed():
    current_user = get_current_user()
    
    # Get pagination parameters
    limit = int(request.args.get('limit', 20))
    before = request.args.get('before')
    
    # Base query - posts from friends and self
    friend_ids = [friend.id for friend in current_user.friends]
    friend_ids.append(current_user.id)
    
    query = Post.query.filter(
        Post.user_id.in_(friend_ids),
        # Don't show ONLY_ME posts from friends
        ~((Post.privacy == PrivacyType.ONLY_ME) & (Post.user_id != current_user.id))
    ).order_by(Post.created_at.desc())
    
    # Apply pagination
    if before:
        # Assuming 'before' is a cursor based on post ID
        # In a real app, you'd need to decode this cursor
        post_id = int(before)
        reference_post = Post.query.get(post_id)
        if reference_post:
            query = query.filter(Post.created_at < reference_post.created_at)
    
    posts = query.limit(limit).all()
    
    # Get next cursor if more posts exist
    next_cursor = None
    if len(posts) == limit:
        next_post = query.offset(limit).first()
        if next_post:
            next_cursor = str(next_post.id)
    
    result = {
        "posts": [post_to_dict(post) for post in posts],
    }
    
    if next_cursor:
        result["pagination"] = {
            "nextCursor": next_cursor
        }
    
    return jsonify(result), 200

# Comment routes
@app.route('/api/v1/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = get_current_user()
    
    # Check if user can comment on this post
    if post.privacy == PrivacyType.ONLY_ME and post.user_id != current_user.id:
        raise APIError("FORBIDDEN", "You don't have permission to comment on this post", 403)
    
    if post.privacy == PrivacyType.FRIENDS and post.user_id != current_user.id:
        if not current_user.is_friend(post.author):
            raise APIError("FORBIDDEN", "You don't have permission to comment on this post", 403)
    
    data = request.get_json()
    
    # Check if required fields are present
    if 'content' not in data:
        raise APIError("VALIDATION_ERROR", "Content is required")
    
    # Create comment
    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=data['content']
    )
    
    db.session.add(comment)
    db.session.commit()
    
    # Add media if provided
    if 'mediaUrl' in data:
        media = Media(
            url=data['mediaUrl'],
            content_id=comment.id,
            content_type='COMMENT'
        )
        db.session.add(media)
        db.session.commit()
    
    # Create notification for post author if it's not the commenter
    if post.user_id != current_user.id:
        create_notification(
            user_id=post.user_id,
            actor_id=current_user.id,
            notification_type=NotificationType.POST_COMMENT,
            content_id=post.id,
            content_type='POST',
            content_preview=comment.content[:97] + '...' if len(comment.content) > 100 else comment.content
        )
    
    return jsonify(comment_to_dict(comment)), 201

# @app.route('/api/v1/posts/<int:post_id>/comments', methods=['GET'])
# @jwt_required()
# def get_comments(post_id):
#     post = Post.query.get_or_404(post_id)
#     current_user = get_current_user()
#     
#     # Check if user can view this post
#     if post.privacy == PrivacyType.