import random
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import requests


def fetch_random_ctv_news_article_paragraphs(
        xml_url="https://www.ctvnews.ca/rss/ctvnews-ca-top-stories-public-rss-1.822009"):
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


# Example usage:
random_article_paragraphs = fetch_random_ctv_news_article_paragraphs()
print(random_article_paragraphs)
