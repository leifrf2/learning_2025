"""
You are provided with a helper function, get_links(url), which fetches the HTML content of a given URL and extracts all the hyperlinks present in the document. Your task is to implement a web crawler that, given a seed_url, systematically explores all reachable links and returns a unique set of URLs that can be visited.

The crawler should adhere to the following constraints:

Domain Restriction: It should only consider URLs that belong to the same domain as the seed_url. External links should be ignored.
Fragment Handling: Any fragment identifiers (i.e., the portion of the URL after #) should be disregarded when considering uniqueness.
Part 2: Write a multi-threaded version of the same crawler.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links(base_url):
    links = []
    
    try:
        # Fetch the HTML content
        response = requests.get(base_url, timeout=5)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags and extract href attributes
        for a_tag in soup.find_all("a", href=True):
            link = a_tag["href"]
            absolute_url = urljoin(base_url, link)  # Resolve relative URLs
            links.append(absolute_url)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")

    return links

# Example usage:
url = "<https://example.com>"
print(get_links(url))
"""