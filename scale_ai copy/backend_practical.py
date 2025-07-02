### Focus on progress rather than perfection; iterative improvements are encouraged. ###
### Keep your solutions straightforward – there’s no need for complex optimizations unless prompted. ###

import datetime
import validators
from pprint import pprint
from dataclasses import dataclass
from typing import Any, Dict, List
import requests
from requests import Response
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__": 
    print("My IP Address is:", 
    requests.get("https://api.ipify.org?format=json").json()['ip']) 

def hello_world():
    print("hello world")
