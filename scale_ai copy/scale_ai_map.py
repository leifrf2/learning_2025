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

# planning a multi-week ski trip
# drive as little as polsible
# find optimal route between resorts
# the order is not fixed
### in part like a traveling salesman problem
### (come back to this optimzation later)
# use google maps to simplify this trip and future trips
# only going between resorts

### part 1
# translate his address and resorts into place_ids
# will use place_ids in the rest of the platforms
# https://developers.google.com/maps/documentation/places/web-service/overview

## two versions of the places API
# old one and new old
# both work, but the new one is easier to use

### make sure to use the proxy

logging.basicConfig(level=logging.DEBUG)


# old key: KEY= "1741021164.i0fZE4/BC8qBk0KayUfGD3N3DySkyHeN1cTR1ZPuJ6A="
KEY = "1741025125.sTxUIsuzq8GQPRe5K+nMSvYyYsoHi+J0FZYO6dkEBXM="

session = requests.Session()
session.headers.update(
    {
        "authorization": KEY, 
        # come back to field mask
        "x-goog-fieldmask": "*"
     }
    )

# for the purposes of this interview, we are going to access the Maps APIs through a proxy
# e.g. if you would normally make a request to https://translation.googleapis.com/language/translate/v2,
# instead make a request to https://translation.googleapis.com.maps-interview-proxy.scale.com/language/translate/v2
# https://places.googleapis.com/v1/places/

# place_ids
# https://developers.google.com/maps/documentation/places/web-service/place-id
# ChIJgUbEo8cfqokR5lP9_Wh_DaM


V1_PLACES_ROUTE = "/v1/places/"

PROXY_SUFFIX = ".maps-interview-proxy.scale.com"
BASE_URL = "https://places.googleapis.com"
COMPLETE_URL = BASE_URL + PROXY_SUFFIX
PLACES_ENDPOINT = COMPLETE_URL + "/v1/places"

# 1. post to places:searchText with textQuery in data
# in response:
# json['places'][0]['id']
# for this interview, assume the first index is always the correct one
# TODO: error handling
def get_place_id(textQuery: str) -> str:
    endpoint: str = COMPLETE_URL + "/v1/places:searchText"
    post_data: Dict = { "textQuery" : textQuery }
    response = session.post(endpoint, data=post_data)
    return response.json()['places'][0]['id']


# Eiw1NTYgSmFja3NvbiBTdCwgU2FuIEZyYW5jaXNjbywgQ0EgOTQxMTEsIFVTQSIxEi8KFAoSCfcD3ij1gIWAETxbJwEZcXysEKwEKhQKEgnDfhDfw4CFgBFQsXmMN77xwQ
START_LOCATION = "556 Jackson St, San Francisco CA 94109"
RESORTS = [
    "Palisades Tahoe",
    "Kirkwood Mountain Resort",
    "Jackson Hole Mountain Resort",
    "A-basin",
]

# for part 1
# convert each of START_LOCATION and each of RESORTS to place_ids

def get_place_id_map():

    location_placeid_map: Dict[str, str] = dict()

    location_placeid_map[START_LOCATION] = get_place_id(START_LOCATION)
    for resort in RESORTS:
        location_placeid_map[resort] = get_place_id(resort)
    
    return location_placeid_map


# for part 2
# now that we have the place ids
# determine the optimal to visit these locations
# use the route api to determine the time it takes to drive between each of these locations
# just getting the travel times, not doing optimizations
#### this includes going from A to B AND from B to A

# https://routes.googleapis.com/directions/v2:computeRoutes
### use the proxy
# we can do route with multiple stops

# found how to use place_id with route here:
# https://stackoverflow.com/questions/36763790/google-maps-api-js-create-a-route-using-placeid-in-waypoints

def get_travel_time(origin_place_id: str, destination_place_id: str) -> str:
    endpoint: str = "https://routes.googleapis.com.maps-interview-proxy.scale.com/directions/v2:computeRoutes"
    post_data: Dict = {
        "origin" : {
            "placeId" : origin_place_id
        },
        "destination" : {
            "placeId" : destination_place_id
        },
        "travelMode": "DRIVE",
        #"routingPreference": "TRAFFIC_AWARE",
        #"computeAlternativeRoutes": False,
        #"routeModifiers": {
        #    "avoidTolls": False,
        #    "avoidHighways": False,
        #    "avoidFerries": False
        #},
        #"languageCode": "en-US",
        #"units": "IMPERIAL"
    }

    # handle this response
    response = session.post(endpoint, json=post_data)


    #{
    #  "routes": [
    #    {
    #      "distanceMeters": 772,
    #      "duration": "165s",
    #      "polyline": {
    #        "encodedPolyline": "ipkcFfichVnP@j@BLoFVwM{E?"
    #      }
    #    }
    #  ]
    #}
    ### this is in format of {int}{time_unit}, need to parse
    travel_time_response = response.json()['routes'][0]['duration']

    travel_time_unit: str = travel_time_response[-1]
    if travel_time_unit == "s":
        return int(travel_time_response[:-1])
    else:
        raise ValueError(f"unknown time_travel_unit: {travel_time_unit}")


travel_map = get_place_id_map()


@dataclass
class Route:
    origin: str
    desintaiton: str
    duration: int

travel_times_dict = dict()
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

