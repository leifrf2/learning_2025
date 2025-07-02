from pprint import pprint
from dataclasses import dataclass
from typing import Dict
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

KEY = "1741025125.sTxUIsuzq8GQPRe5K+nMSvYyYsoHi+J0FZYO6dkEBXM="
PROXY_SUFFIX = ".maps-interview-proxy.scale.com"

START_LOCATION = "556 Jackson St, San Francisco CA 94109"
RESORTS = [
    "Palisades Tahoe",
    "Kirkwood Mountain Resort",
    "Jackson Hole Mountain Resort",
    "A-basin",
]

@dataclass
class Route:
    origin: str
    desintaiton: str
    duration: int

session = requests.Session()
session.headers.update(
    {
        "authorization": KEY, 
        "x-goog-fieldmask": "*"
     }
    )

def get_place_id(textQuery: str) -> str:
    endpoint: str = "https://places.googleapis.com" + PROXY_SUFFIX + "/v1/places:searchText"
    post_data: Dict = { "textQuery" : textQuery }
    response = session.post(endpoint, data=post_data)
    return response.json()['places'][0]['id']


def get_place_id_map():
    location_placeid_map: Dict[str, str] = dict()

    location_placeid_map[START_LOCATION] = get_place_id(START_LOCATION)
    for resort in RESORTS:
        location_placeid_map[resort] = get_place_id(resort)
    
    return location_placeid_map


def get_travel_time(origin_place_id: str, destination_place_id: str) -> str:
    endpoint: str = "https://routes.googleapis.com.maps-interview-proxy.scale.com/directions/v2:computeRoutes"
    post_data: Dict = {
        "origin" : {
            "placeId" : origin_place_id
        },
        "destination" : {
            "placeId" : destination_place_id
        },
        "travelMode": "DRIVE"
    }

    # handle this response
    response = session.post(endpoint, json=post_data)

    ### this is in format of {int}{time_unit}, need to parse
    travel_time_response = response.json()['routes'][0]['duration']

    travel_time_unit: str = travel_time_response[-1]
    if travel_time_unit == "s":
        return int(travel_time_response[:-1])
    else:
        raise ValueError(f"unknown time_travel_unit: {travel_time_unit}")

travel_map = get_place_id_map()

travel_times = list()
for origin_place_id in travel_map.values():
    for destination_place_id in travel_map.values():
        travel_time = get_travel_time(origin_place_id, destination_place_id)
        travel_times.append(
            Route(
                origin=origin_place_id,
                desintaiton=destination_place_id,
                duration=travel_time
            )
        )

pprint(travel_times)

