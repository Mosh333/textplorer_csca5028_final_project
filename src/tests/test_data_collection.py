import unittest
from unittest.mock import patch, Mock
from src.data_collection.fetch_random_news_article import fetch_random_ctv_news_article_paragraphs, \
    fetch_random_abcnews_post_article_paragraphs, fetch_random_aljazeeera_post_article_paragraphs


class TestFetchRandomNewsArticles(unittest.TestCase):

    # Tests invoking the method directly
    def test_fetch_random_ctv_news_article_paragraphs_direct(self):
        paragraphs, link = fetch_random_ctv_news_article_paragraphs()
        self.assertIsInstance(paragraphs, str)
        self.assertIsInstance(link, str)
        self.assertTrue(link.__contains__("ctvnews.ca"))

    def test_fetch_random_abcnews_post_article_paragraphs_direct(self):
        paragraphs, link = fetch_random_abcnews_post_article_paragraphs()
        self.assertIsInstance(paragraphs, str)
        self.assertIsInstance(link, str)
        self.assertTrue(link.__contains__("abcnews"))

    def test_fetch_random_aljazeeera_post_article_paragraphs_direct(self):
        paragraphs, link = fetch_random_aljazeeera_post_article_paragraphs()

        self.assertIsInstance(paragraphs, str)
        self.assertIsInstance(link, str)
        self.assertTrue(link.__contains__("aljazeera"))

    # Tests using mocking is a massive rabbit hole for the fetching script
    # and the above three tests does an adequate job validating the fetch method is working


# Good practice to include this in unit test files.
if __name__ == '__main__':
    unittest.main()
