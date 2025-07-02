from pprint import pprint
from typing import List, Dict
from sqlalchemy import create_engine, text, inspect
import requests
from app import create_app

API_ENDPOINT = "http://127.0.0.1:5000"

HEADERS = dict()

def login(user_id: int):
    response = requests.post(f'{API_ENDPOINT}/auth/login', json={"user_id" : user_id})
    access_token = response.json()["access_token"]
    HEADERS["Authorization"] = f"Bearer {access_token}"

def get_me() -> Dict:
    response = requests.get(f'{API_ENDPOINT}/users/me', headers=HEADERS)
    return response.json()

def get_authors() -> List[Dict]:
    response = requests.get(f'{API_ENDPOINT}/authors', headers=HEADERS)
    return response.json()

def create_book() -> Dict:
    response = requests.post(
        f'{API_ENDPOINT}/books',
        json={
            "Title": "The First Nap",
            "Author": "Khushboo Sharma",
            "Published Year": 2026,
            "Series": "The Adventures of Jude"
        }
    )
    return response.json()

# doesn't work
def engine_query(query: str):
    engine = create_engine("sqlite:///books.db")
    with engine.connect() as connection:
        res = connection.execute(text("SELECT * FROM sqlite_master")).fetchall()
        pprint(res)
        pprint(inspect(engine).get_table_names())

def main():
    user_id = 1
    login(user_id)
    
    me = get_me()
    pprint(me)

    authors = get_authors()
    pprint(authors)

    created_book = create_book()
    pprint(created_book)


if __name__ == "__main__":
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        data = client.get('/books')
        pprint(data.json)
