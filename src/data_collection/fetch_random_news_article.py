import random
import xml.etree.ElementTree as ET
from typing import Tuple

from bs4 import BeautifulSoup

import requests


def fetch_random_ctv_news_article_paragraphs(
        xml_url: str = "https://www.ctvnews.ca/rss/ctvnews-ca-top-stories-public-rss"
) -> Tuple[str, str]:
    # Fetch the XML content from the URL
    response = requests.get(xml_url)
    if response.status_code != 200:
        print("Failed to fetch XML data from the provided URL.")
        return ""

    # Parse the XML content
    root = ET.fromstring(response.content)

    # Store article links
    article_links = []

    # Iterate over each item in the XML
    for item in root.findall('.//item'):
        # Find the link element under each item
        link_element = item.find('link')
        if link_element is not None:
            link = link_element.text
            # Check if the link is not equal to the excluded link we hardcoded above
            if link != xml_url:
                article_links.append(link)

    # Select a random article link
    random_article_link = random.choice(article_links)

    # Fetch the content of the selected link
    article_response = requests.get(random_article_link)
    if article_response.status_code != 200:
        print(f"Failed to fetch article content from the link: {random_article_link}")
        return []

    # Parse the HTML content of the article
    article_soup = BeautifulSoup(article_response.content, 'html.parser', from_encoding=article_response.encoding)

    # Extract all <p> tag entries in the article
    paragraphs = [p.get_text() for p in article_soup.find_all('p')]

    # String join to convert into a single string
    cleaned_article_text = ''.join(paragraphs)  # pick between '', ' ', and '\n'. None of them are perfect...

    return [cleaned_article_text, random_article_link]


# washington post is flaky because of paywall, will use abcnews, less greedy and no paywall so more stable
# list of abc news feeds: https://abcnews.go.com/Site/page/rss-feeds-3520115
def fetch_random_abcnews_post_article_paragraphs(
        xml_url: str = "https://abcnews.go.com/abcnews/topstories"
) -> Tuple[str, str]:
    try:
        response = requests.get(xml_url, timeout=180)
        if response.status_code != 200:
            print("Failed to fetch XML data from the provided URL.")
            return []
    except requests.Timeout:
        print("Requested ABCNews RSS link timed out while trying to fetch XML timeout")
        return []

    root = ET.fromstring(response.content)
    links = []

    for item in root.findall('.//item'):
        link_element = item.find('link')
        if link_element is not None:
            link = link_element.text
            if "/video/" not in link:
                links.append(link)

    if not links:
        print("No valid article links found.")
        return ["failed", "N/A"]

    random_article_link = random.choice(links)

    try:
        article_response = requests.get(random_article_link, timeout=180)
        if article_response.status_code != 200:
            print(f"Failed to fetch article content from provided URL: {random_article_link}")
            return ["failed", "N/A"]
    except requests.Timeout:
        print(f"Request timed out while fetching ABC News article content: {random_article_link}")
        return ["failed", "N/A"]

    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    paragraphs = [p.get_text() for p in article_soup.find_all('p')]
    cleaned_article_text = ''.join(paragraphs)

    return [cleaned_article_text, random_article_link]


# Extracts links from the given URL and trims off "?traffic_source=rss" from each link.
def fetch_random_aljazeeera_post_article_paragraphs(
        html_url: str = "https://feeder.co/discover/9f94548972/aljazeera-com-default-html"
) -> Tuple[str, str]:
    # Fetch the HTML content from the website
    response = requests.get(html_url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <a> tags with href attribute starting with "https://www.aljazeera.com"
    links = soup.find_all("a", href=lambda href: href and href.startswith("https://www.aljazeera.com"))

    # Extract the links and trim off "?traffic_source=rss" at the end
    trimmed_links = []
    for link in links:
        href = link.get("href")
        if "?traffic_source=rss" in href:
            href = href.split("?traffic_source=rss")[0]  # Trim off "?traffic_source=rss"
        trimmed_links.append(href)

    random_article_link = random.choice(trimmed_links)

    article_response = requests.get(random_article_link)
    if article_response.status_code != 200:
        print(f"Failed to fetch article content from the provided URL: {random_article_link}")
        return ""

    article_soup = BeautifulSoup(article_response.content, 'html.parser')

    paragraphs = [p.get_text() for p in article_soup.find_all('p')]

    cleaned_article_text = ''.join(paragraphs)  # pick between '', ' ', and '\n'. None of them are perfect...

    return [cleaned_article_text, random_article_link]


def check_url_access(url: str) -> None:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Access to {url} is successful.")
        else:
            print(f"Failed to access {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to access {url}. Error: {str(e)}")

# url = "https://abcnews.go.com/International/russia-jails-activist-oleg-orlov-ukraine-war-alexei-navalny-death/story?id=107600667"
# check_url_access(url)

# Example usage:
# ctv_random_article_paragraphs = fetch_random_ctv_news_article_paragraphs()
# print(ctv_random_article_paragraphs)
#
# abcnews_random_article_paragraphs = fetch_random_abcnews_post_article_paragraphs()
# print(abcnews_random_article_paragraphs)
#
# aljazeeera_post_random_article_paragraphs = fetch_random_aljazeeera_post_article_paragraphs()
# print(aljazeeera_post_random_article_paragraphs)
