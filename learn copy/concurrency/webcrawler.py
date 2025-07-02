"""
Our task is to build a web crawler in any programming language, using the provided HtmlParser interface.
We're supposed to build a multi-threaded web crawler that can crawl through all links under the same hostname as the startUrl.
By multi-threaded, it means that we need to design a solution that can work on multiple threads simultaneously and fetch the pages,
rather than fetching one by one.

We're given some constraints on what hostname can be, which is an important clue about the problem.
In our input, we have multiple urls, and a query/url to start with.

Here is a step-by-step visual explanation of how to approach this problem:

Let's consider this simple example input:

urls = [ "http://news.yahoo.com", "http://news.yahoo.com/news", "http://news.google.com" ]

startUrl = "http://news.yahoo.com"

First, our crawler starts from startUrl which is "http://news.yahoo.com" and fetches all its urls using HtmlParser.getUrls(url).
If there are more urls under the same host, it will push them in the queue for further crawling.
So the output will be: "news.yahoo.com" "news.yahoo.com/news"

Then, the crawler, in parallel will consider next url in queue and fetches its urls.
As there is no url, it will not add anything to the queue.

In the end, our final output will be ["news.yahoo.com", "news.yahoo.com/news"]
"""

from typing import List, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

class Solution:

    url_queue: List[str] = list()
    urls_active: Set[str] = set()
    urls_visisted: Set[str] = set()
    queues_lock: Lock = Lock()

    def pop_queue_if_any(self) -> Optional[str]:
        with self.queues_lock:
            if len(self.url_queue) > 0:
                url = self.url_queue.pop()
                self.urls_active.add(url)
                self.urls_visisted.add(url)
                return url
            else:
                return None


    def complete_url(self, url: str, urls_output: List[str]) -> None:
        with self.queues_lock:
            for url_output in urls_output:
                if url_output not in self.urls_visisted:
                    self.url_queue.append(url_output)
            self.urls_active.remove(url)


    def is_done(self) -> bool:
        with self.queues_lock:
            return len(self.url_queue) > 0 or len(self.urls_active) > 0


    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        parallelism: int = 5

        self.url_queue.append(startUrl)

        # htmlParser.GetUrls(current)
        def worker(url: str) -> None:
            urls: List[str] = htmlParser.GetUrls(url)
            self.complete_url(url, urls)

        with ThreadPoolExecutor(max_workers=parallelism) as executor:
            while not self.is_done():
                next_url = self.pop_queue_if_any()
                if next_url:
                    executor.submit(worker, next_url)
            
