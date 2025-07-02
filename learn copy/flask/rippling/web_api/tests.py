from pprint import pprint
import requests
import json

TEST_ENDPOINT = "http://127.0.0.1:5000"

def register_login_test():
    register_data = {
        "birth_date" : "2025-01-01",
        "first_name" : "Leif",
        "last_name" : "Raptis-Firth",
        "email" : "leifrf@gmail.com",
        "password" : "12345"
    }

    output = requests.post(f"{TEST_ENDPOINT}/auth/register", json=register_data)
    pprint(output.json())

    login_data = {
        "email" : "leifrf@gmail.com",
        "password" : "12345"
    }

    output = requests.post(f"{TEST_ENDPOINT}/auth/login", json=login_data)
    pprint(output.json())

    token = output.json()["token"]

    headers = {
        "Authorization" : f"Bearer {token}"
    }

    post_data = {
        "content" : "hello world"
    }

    output = requests.post(f"{TEST_ENDPOINT}/questions", json=post_data, headers=headers)
    pprint(output.json())


def run_tests():
    register_login_test()

run_tests()