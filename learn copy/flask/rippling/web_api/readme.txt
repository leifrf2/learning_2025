Problem: Build Quora
Start: 4:23PM
End: 5:23PM


==== System Description ====

Okay, what is Quora?
It's a forum where users can make a post, and other users can respond to that post.
Post content is text, potentially a lot of text.
It can include links
Posts have a score based on upvote/downvote.

It's more complex than that.
The taxonomy is:
Question
> answer
    - upvotes
    - author
    > comments

Users can also bookmark posts in their profile
Users can follow other users.
Users can search for posts.

User profiles:
- name
- institution / place of work
- join date / years on Quora
- number of answers
- number of answer views

Client side:
Users have a set of related questions to a posed question.
The returned questions have different sort options (Recommended, Upvotes, Recent)



==== Data Model ====

Question
- id
- user_id
- created_date
- updated_date
- content
: create_question(text) # requires user logged in
: update_question(id, text) # requires user logged in and be author
: get_question(id)
: get_answers(id, count, sort_logic)
: get_related(id, count, sort_logic)

Answer
- id 
- question_id
- user_id
- content
- created_date
- updated_date
- upvotes
- views
: create_answer(question_id, text) # requires user logged in
: update_answer(id, text) # requires user logged in and be author
: get_answer(answer_id)
: upvote_answer(id) # requires user logged in
: downvote_answer(id) # requires user logged in
: get_comments(id, count) # always chronological


Comment
- id
- answer_id
- user_id
- content
- created_date
- updated_date
: create_comment(answer_id, text) # requires user logged in
: update_comment(id, text)  # requires user logged in and be author
: get_comment(id)


User
- id
- picture_url
- first_name
- last_name
- email
- institution
- created_date
- updated_date
: create_user(first_name, last_name, institution, email)
: update_user(id, {kwargs}) # requires user logged in
: follow_user(id, user_id)  # requires user logged in


Auth
: login(email)


Follows (Table)
- user_id_follower
- user_id_followee
