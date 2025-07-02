import pytest
from app import app
from config import db
from pprint import pprint
import requests
import json

TEST_ENDPOINT = "http://127.0.0.1:5000"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_database():
    with app.app_context():
        # Create test data
        test_data = [
            
        ]

        db.session.add_all(test_data)
        db.session.commit()
        yield

        for item in test_data:
            db.session.remove(item)


def test_with_data(client, setup_database):
    pass

def test_client(client):
    pass
    