from typing import Dict, List, Optional, Set
from datetime import date, datetime

class ToDictAble:
    def to_dict(self):
        result = dict()
        for k, v in vars(self).items():
            result[k] = v
        
        return result

class User(ToDictAble):
    
    def __init__(self,
                    id,
                    first_name: str,
                    last_name: str,
                    email: str,
                    birth_date: date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.created_date = datetime.utcnow()

class Post(ToDictAble):

    def __init__(self,
                    id: int, 
                    user_id: int,
                    content: str):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.created_date = datetime.utcnow()

REACIONTYPE_HEART = 0
REACTIONTYPE_LAUGH = 1
REACTIONTYPE_SAD = 2

class Reaction(ToDictAble):

    def __init__(self,
                 id: int,
                 user_id: int,
                 post_id: int,
                 reaction_type: int):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        
        if reaction_type not in [REACIONTYPE_HEART, REACTIONTYPE_LAUGH, REACTIONTYPE_SAD]:
            raise ValueError(f"unsupported reaction type {reaction_type}.\
                              must be one of {[REACIONTYPE_HEART, REACTIONTYPE_LAUGH, REACTIONTYPE_SAD]}")

        self.reaction_type = reaction_type
        self.created_date = datetime.utcnow()

class FacebookManager:

    def __init__(self):
        self.next_user_id: int = 0
        self.next_post_id: int = 0
        self.next_reaction_id: int = 0

        self.users: Dict[int, User] = dict()
        self.posts: Dict[int, Post] = dict()

        self.user_reaction_map: Dict[int, Set[Reaction]] = dict()
        self.post_reaction_map: Dict[int, Set[Reaction]] = dict()

        self.user_emails: Set[str] = set()

        self.current_user: Optional[User] = None


    def set_current_user(self, user_id: int):
        if user_id not in self.users.keys():
            raise f"user_id is not in set of known users"
        else:
            self.current_user = self.users[user_id]


    def email_in_use(self, email: str) -> bool:
        return email in self.user_emails


    def get_next_user_id(self):
        next_id = self.next_user_id
        self.next_user_id += 1
        return next_id


    def get_next_post_id(self):
        next_id = self.next_post_id
        self.next_post_id += 1
        return next_id


    def get_next_reaction_id(self):
        next_id = self.next_reaction_id
        self.next_reaction_id += 1
        return next_id


    # email must be unique
    def add_user(self, first_name: str, last_name: str, email: str, birth_date: date):
        if self.email_in_use(email):
            raise ValueError(f"email is already in use. it must be unique")

        next_id = self.get_next_user_id()
        new_user = User(
            next_id,
            first_name,
            last_name,
            email,
            birth_date
        )

        self.users[next_id] = new_user

        self.user_emails.add(email)

        return self.users[next_id]


    def add_post(self, user_id: int , content: str):
        if user_id not in self.users.keys():
            raise ValueError(f"Unknown user_id: {user_id}")
        
        next_id = self.get_next_post_id()
        new_post = Post(next_id, user_id, content)

        self.posts[next_id] = new_post


    def add_reaction(self, user_id: int , post_id: int , reaction_type: int):
        if not post_id in self.posts.keys():
            raise ValueError(f"post doesn't exist: {post_id}")

        if not user_id in self.users.keys():
            raise ValueError(f"user doesn't exist: {user_id}")
        
        next_id = self.get_next_reaction_id()
        new_reaction = Reaction(
            next_id,
            user_id,
            post_id,
            reaction_type
        )

        if user_id not in self.user_reaction_map.keys():
            self.user_reaction_map[user_id] = set()

        if post_id not in self.post_reaction_map.keys():
            self.post_reaction_map[post_id] = set()

        self.user_reaction_map[user_id].add(new_reaction)
        self.post_reaction_map[post_id].add(new_reaction)


    def get_user_reactions(self, user_id: int) -> List[Reaction]:
        return self.user_reaction_map.get(user_id, list())


    def get_post_reactions(self, post_id: int) -> List[Post]:
        return self.post_reaction_map.get(post_id, list())

facebook_manager: FacebookManager = FacebookManager()