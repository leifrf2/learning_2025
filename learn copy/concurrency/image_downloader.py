"""
https://unsplash.com/oauth/applications/726677

Note that only the json requests (i.e., those to api.unsplash.com) are counted.
Image file requests (images.unsplash.com) do not count against your rate limit.
"""


import math
from dataclasses import dataclass
import threading
import time
import os
from pathlib import Path
import json
import concurrent.futures
import logging
from typing import Any, Dict, Iterable, Optional, List, Tuple
import requests
from requests import Response
from requests.auth import HTTPBasicAuth
import requests_oauthlib
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MAX_FETCH: int = 30


@dataclass
class ImageDownloaderConifg:
    app_name : str
    application_id : int
    access_key : str
    secret_key : str
    rate_limit_h: int


@dataclass
class RateLimit:
    rate_limit_h: int
    rate_limit_remaining_h: int


def get_rate_limits_from_response(response: Response) -> RateLimit:
    return RateLimit(
        rate_limit_h=response.headers['X-Ratelimit-Limit'],
        rate_limit_remaining_h=response.headers['X-Ratelimit-Remaining']
    )


@dataclass
class UnsplashImage:
    id: str
    created_at: datetime
    updated_at: datetime
    width: int
    height: int
    downloads: int
    likes: int
    description: str
    url_full: str
    download_location: str
    user_id: str
    location_country: str


def read_image_downloader_config(file_path: str) -> ImageDownloaderConifg:
    with open(file_path, 'r') as file:
        file_dict = json.loads(file.read())
        return ImageDownloaderConifg(
            app_name=file_dict['app_name'],
            application_id=file_dict['application_id'],
            access_key=file_dict['access_key'],
            secret_key=file_dict['secret_key'],
            rate_limit_h=file_dict['rate_limit_h']
        )


class ImageDownloader:
    api_root: str = "https://api.unsplash.com"

    def __init__(self, config:ImageDownloaderConifg):
        self.config = config
        self.session = None

        self.image_download_queue: List[UnsplashImage] = list()
        self.image_download_lock: threading.Lock  = threading.Lock()


    def get_session(self) -> requests.Session:
        if not self.session:
            self.session = requests.session()

            self.session.headers = {
                "Accept-Version" : "v1",
                "Authorization" : f"Client-ID {self.config.access_key}"
            }

            retry_logic = Retry(total=3, backoff_factor=2)
            adapter = HTTPAdapter(max_retries=retry_logic, pool_maxsize=50)
            self.session.mount(prefix="https://", adapter=adapter)
        
        # clear params for each session
        self.session.params = {}
        return self.session
    

    def response_element_to_unsplash_image(self, response: dict) -> UnsplashImage:
        def convert_datetime(response_datetime: str) -> datetime:
            return datetime.strptime(response_datetime, "%Y-%m-%dT%H:%M:%SZ"),
    
        return UnsplashImage(
                created_at=convert_datetime(response['created_at']),
                description=response.get('description'),
                download_location=response['links']['download_location'],
                downloads=int(response['downloads']),
                height=int(response['height']),
                id=response['id'],
                likes=int(response['likes']),
                location_country=response['location']['name'],
                updated_at=convert_datetime(response['updated_at']),
                url_full=response['urls']['full'],
                user_id=response['user']['id'],
                width=int(response['width'])
            )


    def get_random_image(self) -> UnsplashImage:
        return self.get_random_images(count=1)[0]


    def get_random_images(self, count=10) -> List[UnsplashImage]:
        api_target = self.api_root + "/photos/random"
        response = self.get_session().get(url=api_target, params= { "count" : count })
        logger.info(get_rate_limits_from_response(response=response))

        if response.status_code in [200, 201]:
            # good image
            json: List[Dict] = response.json()
            return [self.response_element_to_unsplash_image(d) for d in json]
        else:
            # handle error
            pass


    def download_image(self, url_full: str, destination_path: str) -> None:
        logger.debug(f"downloading {url_full} to {destination_path}")
        response = self.get_session().get(url=url_full, stream=True)

        if response.status_code in [200, 201]:
            with open(destination_path, 'wb') as writer:
                writer.write(response.content)
        
        logger.debug(f"completed {url_full}")


    def download_images(self, url_destination_pairs: List[Tuple[str, str]], parallelism=5):
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallelism) as executor:
            futures: List[concurrent.futures.Future] = list()
            for url, dest in url_destination_pairs:
                future = executor.submit(self.download_image, url, dest)
                futures.append(future)
            
            for future in futures:
                future.result()


    def get_random_images_and_enqueue(self, count=10):
        random_images = self.get_random_images(count=count)
        with self.image_download_lock:
            self.image_download_queue.extend(random_images)


    def start_producer_manager(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            pass
            

    def start_consumer_manager(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            pass


def main(config_path: str, image_count: int = 300, parallelism = 30) -> None:

    image_downloader = ImageDownloader(config=config)


    config = read_image_downloader_config(config_path)
    image_downloader = ImageDownloader(config=config)

    fetches_to_do = math.ceil(image_count / MAX_FETCH)

    download_dir = Path.joinpath(Path.home(), "scratch", "image_downloader_6")
    Path.mkdir(download_dir, parents=True, exist_ok=True)

    def get_download_path(image_id: str) -> str:
        return Path.joinpath(download_dir, f"{image_id}.png")

    producer_manager_thread = threading.Thread(target=producer_manager,args=[image_downloader])
    consumer_manager_thread = threading.Thread(target=consumer_manager,args=[image_downloader])

    start_time = time.time()
    producer_manager_thread.start()
    consumer_manager_thread.start()
    end_time = time.time()

    print(f"elapsed for {image_count} images with {parallelism} threads: {end_time-start_time:0.4}")


if __name__=="__main__":
    config_path: str = "concurrency/unsplash_secrets.json"
    main(config_path)
