import logging
import requests
import requests.auth
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)

CLIENT_ID: str = "flmhnSESvD12LKaTyzDx8Q"
CLIENT_SECRET: str = "LRN6y_WvIoPTF9J7mKFcGpw7K_zd7A"


client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
post_data = {"grant_type": "password", "username": "foobar487", "password": "reddit!Tht3691215"}
headers = {"User-Agent": "My-Agent/0.1 by leifrf"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
token = response.json()['access_token']

headers = {"Authorization": f"bearer {token}", "User-Agent": "My-Agent/0.1 by leifrf"}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
pprint(response.json())
