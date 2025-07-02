"""
Learnings from this exercise:

The default logging library is REALLY helpful.
It has instrumentation for existing libraries that make debugging much easier.

Use the debug console window for playing with the current memory.
Super helpful. Maybe even go so far as to mutate existing variables for debugging?

pprint, dataclasses, typing are all really helpful for staying organized.

use the requests extension libraries for auth and headers

create a test file for functionality
reference the __name__ support in the main file

maybe keep a .txt file for notes as well along the way

use multi-line editing to quickly create dataclasses from dictionary, and other editing steps.

"""


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

REDIRECT_URI: str = "http://localhost:8080/"
CLIENT_ID: str = "flmhnSESvD12LKaTyzDx8Q"
CLIENT_SECRET: str = "LRN6y_WvIoPTF9J7mKFcGpw7K_zd7A"

@dataclass
class AccessTokenResponse:
    access_token: str
    token_type: str
    scope: str
    expires_in: int

@dataclass
class RedditPost:
    approved_at_utc: Any
    subreddit: str
    selftext: str
    author_fullname: str
    saved: bool
    mod_reason_title: Any
    gilded: int
    clicked: bool
    title: str
    link_flair_richtext: list
    subreddit_name_prefixed: str
    hidden: bool
    pwls: int
    link_flair_css_class: str
    downs: int
    thumbnail_height: int
    top_awarded_type: Any
    hide_score: bool
    name: str
    quarantine: bool
    link_flair_text_color: str
    upvote_ratio: float
    author_flair_background_color: Any
    ups: int
    total_awards_received: int
    media_embed: dict
    thumbnail_width: int
    author_flair_template_id: Any
    is_original_content: bool
    user_reports: list
    secure_media: Any
    is_reddit_media_domain: bool
    is_meta: bool
    category: Any
    secure_media_embed: dict
    link_flair_text: str
    can_mod_post: bool
    score: int
    approved_by: Any
    is_created_from_ads_ui: bool
    author_premium: bool
    thumbnail: str
    edited: bool
    author_flair_css_class: Any
    author_flair_richtext: list
    gildings: dict
    post_hint: str
    content_categories: Any
    is_self: bool
    subreddit_type: str
    created: float
    link_flair_type: str
    wls: int
    removed_by_category: Any
    banned_by: Any
    author_flair_type: str
    domain: str
    allow_live_comments: bool
    selftext_html: Any
    likes: Any
    suggested_sort: Any
    banned_at_utc: Any
    url_overridden_by_dest: str
    view_count: Any
    archived: bool
    no_follow: bool
    is_crosspostable: bool
    pinned: bool
    over_18: bool
    preview: dict
    all_awardings: list
    awarders: list
    media_only: bool
    link_flair_template_id: str
    can_gild: bool
    spoiler: bool
    locked: bool
    author_flair_text: Any
    treatment_tags: list
    visited: bool
    removed_by: Any
    mod_note: Any
    distinguished: Any
    subreddit_id: str
    author_is_blocked: bool
    mod_reason_by: Any
    num_reports: Any
    removal_reason: Any
    link_flair_background_color: str
    id: str
    is_robot_indexable: bool
    report_reasons: Any
    author: str
    discussion_type: Any
    num_comments: int
    send_replies: bool
    contest_mode: bool
    mod_reports: list
    author_patreon_flair: bool
    author_flair_text_color: Any
    permalink: str
    stickied: bool
    url: str
    subreddit_subscribers: int
    created_utc: float
    num_crossposts: int
    media: Any
    is_video: bool

@dataclass
class RedditAccount:
    name: str
    id: str
    created_utc: datetime
    
    is_gold: bool
    is_mod: bool
    
    coins: int
    over_18: bool
    icon_img: str

    link_karma: int
    awardee_karma: int
    comment_karma: int
    total_karma: int
    
    inbox_count: int

class RedditClient:
    api_root: str = "https://www.reddit.com/api/v1/"
    oauth_api_root: str = "https://oauth.reddit.com/"

    get_request_type: str = "GET"
    post_request_type: str = "POST"

    response_kind_listing: str = "Listing"

    subreddit_sort_type_hot: str = "hot"
    subreddit_sort_type_new: str = "new"
    subreddit_sort_type_rising: str = "rising"
    subreddit_sort_type_top: str = "top"
    subreddit_sort_type_controversial: str = "controversial"

    _subreddit_sort_types: List[str] = [
        subreddit_sort_type_hot,
        subreddit_sort_type_new,
        subreddit_sort_type_rising,
        subreddit_sort_type_top,
        subreddit_sort_type_controversial
    ]

    data: Dict[str, str] = {
        "grant_type": "password",
        "username": "foobar487",
        "password": "reddit!Tht3691215"
    }

    headers: Dict[str, str] = {
        "User-Agent": "My-Agent/0.1 by leifrf"
    }

    def __init__(self, client_id:str =CLIENT_ID, client_secret: str =CLIENT_SECRET, access_token: AccessTokenResponse = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

        if self.access_token:
            self._add_access_token_to_headers(self.access_token.access_token)

    # handle if access token is not yet generated
    def _submit_request(self, url: str, request_type: str, data: Dict[str, str] = {}, headers: Dict[str, str] = {}, params: Dict[str, str] = {}) -> Response:
        if not validators.url(url):
            raise ValueError(f"Invalid url: {url}")

        data = self.data | data
        headers = self.headers | headers

        session = requests.Session()
        retries = Retry(total=4, backoff_factor=1, status_forcelist=[429, 401])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        request_result: Response = None

        if request_type.upper() == self.get_request_type:
            request_result = session.get(url, headers=headers, params=params)
        elif request_type.upper() == self.post_request_type:
            auth: HTTPBasicAuth = HTTPBasicAuth(self.client_id, self.client_secret)
            request_result = session.post(url, data=data, headers=headers, auth=auth)
        else:
            raise ValueError(F"Unsupported request_type: {request_type}")

        return request_result

    def _add_access_token_to_headers(self, access_token_value: str) -> None:
        self.headers['Authorization'] = f"bearer {access_token_value}"

    def _get_access_token(self) -> AccessTokenResponse:
        reddit_access_token_url: str = self.api_root + "access_token"

        x: Response = self._submit_request(reddit_access_token_url, self.post_request_type)

        if x.status_code == 200:
            result = x.json()
            if 'error' in result.keys():
                print(f"error: {result['error']}")
            else:
                return AccessTokenResponse(
                    access_token=result['access_token'],
                    token_type=result['token_type'],
                    expires_in=result['expires_in'],
                    scope=result['scope']
                    )

    def fetch_access_token(self) -> None:
        if self.access_token is None:
            self.access_token = self._get_access_token()
        
        self._add_access_token_to_headers(self.access_token.access_token)

    # would do generics here if using py3.12+
    def _process_listing_response(self, response: Response) -> List:
        content: Dict = response.json()

        if content['kind'] != self.response_kind_listing:
            raise ValueError(f"Cannot process a response of kind {content['kind']}. Must be of kind {self.response_kind_listing}")
        
        reddit_posts: List[RedditPost] = list()
        for post in content['data']['children']:
            post_data = post['data']
            reddit_posts.append(
                RedditPost(
                    approved_at_utc = post_data.get("approved_at_utc", None),
                    subreddit = post_data.get("subreddit", None),
                    selftext = post_data.get("selftext", None),
                    author_fullname = post_data.get("author_fullname", None),
                    saved = post_data.get("saved", None),
                    mod_reason_title = post_data.get("mod_reason_title", None),
                    gilded = post_data.get("gilded", None),
                    clicked = post_data.get("clicked", None),
                    title = post_data.get("title", None),
                    link_flair_richtext = post_data.get("link_flair_richtext", None),
                    subreddit_name_prefixed = post_data.get("subreddit_name_prefixed", None),
                    hidden = post_data.get("hidden", None),
                    pwls = post_data.get("pwls", None),
                    link_flair_css_class = post_data.get("link_flair_css_class", None),
                    downs = post_data.get("downs", None),
                    thumbnail_height = post_data.get("thumbnail_height", None),
                    top_awarded_type = post_data.get("top_awarded_type", None),
                    hide_score = post_data.get("hide_score", None),
                    name = post_data.get("name", None),
                    quarantine = post_data.get("quarantine", None),
                    link_flair_text_color = post_data.get("link_flair_text_color", None),
                    upvote_ratio = post_data.get("upvote_ratio", None),
                    author_flair_background_color = post_data.get("author_flair_background_color", None),
                    ups = post_data.get("ups", None),
                    total_awards_received = post_data.get("total_awards_received", None),
                    media_embed = post_data.get("media_embed", None),
                    thumbnail_width = post_data.get("thumbnail_width", None),
                    author_flair_template_id = post_data.get("author_flair_template_id", None),
                    is_original_content = post_data.get("is_original_content", None),
                    user_reports = post_data.get("user_reports", None),
                    secure_media = post_data.get("secure_media", None),
                    is_reddit_media_domain = post_data.get("is_reddit_media_domain", None),
                    is_meta = post_data.get("is_meta", None),
                    category = post_data.get("category", None),
                    secure_media_embed = post_data.get("secure_media_embed", None),
                    link_flair_text = post_data.get("link_flair_text", None),
                    can_mod_post = post_data.get("can_mod_post", None),
                    score = post_data.get("score", None),
                    approved_by = post_data.get("approved_by", None),
                    is_created_from_ads_ui = post_data.get("is_created_from_ads_ui", None),
                    author_premium = post_data.get("author_premium", None),
                    thumbnail = post_data.get("thumbnail", None),
                    edited = post_data.get("edited", None),
                    author_flair_css_class = post_data.get("author_flair_css_class", None),
                    author_flair_richtext = post_data.get("author_flair_richtext", None),
                    gildings = post_data.get("gildings", None),
                    post_hint = post_data.get("post_hint", None),
                    content_categories = post_data.get("content_categories", None),
                    is_self = post_data.get("is_self", None),
                    subreddit_type = post_data.get("subreddit_type", None),
                    created = post_data.get("created", None),
                    link_flair_type = post_data.get("link_flair_type", None),
                    wls = post_data.get("wls", None),
                    removed_by_category = post_data.get("removed_by_category", None),
                    banned_by = post_data.get("banned_by", None),
                    author_flair_type = post_data.get("author_flair_type", None),
                    domain = post_data.get("domain", None),
                    allow_live_comments = post_data.get("allow_live_comments", None),
                    selftext_html = post_data.get("selftext_html", None),
                    likes = post_data.get("likes", None),
                    suggested_sort = post_data.get("suggested_sort", None),
                    banned_at_utc = post_data.get("banned_at_utc", None),
                    url_overridden_by_dest = post_data.get("url_overridden_by_dest", None),
                    view_count = post_data.get("view_count", None),
                    archived = post_data.get("archived", None),
                    no_follow = post_data.get("no_follow", None),
                    is_crosspostable = post_data.get("is_crosspostable", None),
                    pinned = post_data.get("pinned", None),
                    over_18 = post_data.get("over_18", None),
                    preview = post_data.get("preview", None),
                    all_awardings = post_data.get("all_awardings", None),
                    awarders = post_data.get("awarders", None),
                    media_only = post_data.get("media_only", None),
                    link_flair_template_id = post_data.get("link_flair_template_id", None),
                    can_gild = post_data.get("can_gild", None),
                    spoiler = post_data.get("spoiler", None),
                    locked = post_data.get("locked", None),
                    author_flair_text = post_data.get("author_flair_text", None),
                    treatment_tags = post_data.get("treatment_tags", None),
                    visited = post_data.get("visited", None),
                    removed_by = post_data.get("removed_by", None),
                    mod_note = post_data.get("mod_note", None),
                    distinguished = post_data.get("distinguished", None),
                    subreddit_id = post_data.get("subreddit_id", None),
                    author_is_blocked = post_data.get("author_is_blocked", None),
                    mod_reason_by = post_data.get("mod_reason_by", None),
                    num_reports = post_data.get("num_reports", None),
                    removal_reason = post_data.get("removal_reason", None),
                    link_flair_background_color = post_data.get("link_flair_background_color", None),
                    id = post_data.get("id", None),
                    is_robot_indexable = post_data.get("is_robot_indexable", None),
                    report_reasons = post_data.get("report_reasons", None),
                    author = post_data.get("author", None),
                    discussion_type = post_data.get("discussion_type", None),
                    num_comments = post_data.get("num_comments", None),
                    send_replies = post_data.get("send_replies", None),
                    contest_mode = post_data.get("contest_mode", None),
                    mod_reports = post_data.get("mod_reports", None),
                    author_patreon_flair = post_data.get("author_patreon_flair", None),
                    author_flair_text_color = post_data.get("author_flair_text_color", None),
                    permalink = post_data.get("permalink", None),
                    stickied = post_data.get("stickied", None),
                    url = post_data.get("url", None),
                    subreddit_subscribers = post_data.get("subreddit_subscribers", None),
                    created_utc = post_data.get("created_utc", None),
                    num_crossposts = post_data.get("num_crossposts", None),
                    media = post_data.get("media", None),
                    is_video = post_data.get("is_video", None)
                )
            )

        return reddit_posts

    def fetch_me(self) -> RedditAccount:
        url: str = self.oauth_api_root + "api/v1/me"
        response = self._submit_request(url, request_type=self.get_request_type).json()
        return RedditAccount(
            name=response['name'],
            id=response['id'],
            created_utc=datetime.datetime.fromtimestamp(response['created_utc'], datetime.timezone.utc),
            is_gold=response['is_gold'],
            is_mod=response['is_mod'],
            coins=response['coins'],
            over_18=response['over_18'],
            icon_img=response['icon_img'],
            link_karma=response['link_karma'],
            awardee_karma=response['awardee_karma'],
            comment_karma=response['comment_karma'],
            total_karma=response['total_karma'],
            inbox_count=response['inbox_count']
        )

    def _fetch_post_listing(self, subreddit: str, sort_type: str, post_count: int = None) -> List[RedditPost]:
        if sort_type not in self._subreddit_sort_types:
            raise ValueError(f"sort_type must be one of {self._subreddit_sort_types}")

        if post_count <= 0:
            raise ValueError(f"post_count must be a positive integer.")

        url: str = f"{self.oauth_api_root}r/{subreddit}/{sort_type}"

        params: Dict[str, str] = dict()
        if post_count:
            params['limit'] = str(post_count)

        response = self._submit_request(url, self.get_request_type, params=params)
        if response.status_code == 200:
            return self._process_listing_response(response)
        else:
            raise Exception(f"Failed to get {sort_type} posts for subreddit {subreddit}")

    def fetch_new(self, subreddit: str, post_count: int = None):
        return self._fetch_post_listing(subreddit, self.subreddit_sort_type_new, post_count)

    def fetch_top(self, subreddit: str, post_count: int = None):
        return self._fetch_post_listing(subreddit, self.subreddit_sort_type_top, post_count)

    def fetch_rising(self, subreddit: str, post_count: int = None):
        return self._fetch_post_listing(subreddit, self.subreddit_sort_type_rising, post_count)

    def fetch_controversial(self, subreddit: str, post_count: int = None):
        return self._fetch_post_listing(subreddit, self.subreddit_sort_type_controversial, post_count)

    def fetch_hot(self, subreddit: str, post_count: int = None):
        return self._fetch_post_listing(subreddit, self.subreddit_sort_type_hot, post_count)

temp_token = AccessTokenResponse(
    access_token='eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzQwMzQyODY1LjQxMjE5MiwiaWF0IjoxNzQwMjU2NDY1LjQxMjE5MiwianRpIjoidzlGd2Z0OEZJZENHbnR1b0RjZmw1NkhwUHVESTdRIiwiY2lkIjoiZmxtaG5TRVN2RDEyTEthVHl6RHg4USIsImxpZCI6InQyXzd0ZjQ5dmRkIiwiYWlkIjoidDJfN3RmNDl2ZGQiLCJsY2EiOjE1OTgxNTE3MDIyMDQsInNjcCI6ImVKeUtWdEpTaWdVRUFBRF9fd056QVNjIiwiZmxvIjo5fQ.jb5lNRlRP8K8N6CzdNVAlCcvLjAoEVB5xPsCez0jBwCtcdRgLswD7e24_YPUo6N7LgydV8W_QcgJ-Qldj-UuaSLMyCwvrcMAUkhh0W0Mo0pEoTM1RsaxyumY389DqO1SOb6JtnQx1Yn6YMuZZLVeBiA1WlOseAuXn1UuFAe1I-hqLKzq3qFwqTm1RnT7gPMGoKnCXkhM4AUnACIk7q0W89A0hJ3-RAZJOIi_01Ls8zZ65O_Q_aB2_brx4exEhFkNlafYFPzqwaFf8VQc98lEpr-69bW7xmSrO8V7SXtULg_sKtRXCxo89luoYymFTWxeLAaIrJM2DRyH7QzrOJZ0Mg',
    token_type='bearer',
    scope='*',
    expires_in=86400
)

reddit_client: RedditClient = RedditClient(access_token=temp_token)

#me = reddit_client.fetch_me()
APPLE = "apple"
POST_COUNT = 5
_new = reddit_client.fetch_new(APPLE, post_count=POST_COUNT)
_top = reddit_client.fetch_top(APPLE, post_count=POST_COUNT)
_rising =  reddit_client.fetch_rising(APPLE, post_count=POST_COUNT)
_controversial = reddit_client.fetch_controversial(APPLE, post_count=POST_COUNT)
_hot = reddit_client.fetch_hot(APPLE, post_count=POST_COUNT)
print("pause")
pprint(requests.get("https://api.ipify.org?format=json").json()['ip'])
