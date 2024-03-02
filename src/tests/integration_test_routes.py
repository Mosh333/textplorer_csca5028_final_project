import os
import unittest
from unittest.mock import patch
from src.routes import setup_routes  # Import the setup_routes function from routes.py
from src.app import app
from flask import Flask


# MUST SET THE FOLLOWING ENVIRONMENT VARIABLES IN THE TEST RUN OR IT WILL FAIL!!!
# set AWS_ACCESS_KEY_ID=...
# set AWS_SECRET_ACCESS_KEY=...
# set AWS_REGION=us-east-1
# set DYNAMODB_TABLE_NAME=textplorer-nosql-db

class TestRoutesIntegration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_main_route(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_process_input_text_input(self):
        response = self.app.post('/text-analy', data={'selected_option': 'text_input', 'text_input': 'test_text'})
        self.assertEqual(response.status_code, 200)

    # testing the rest of the routes is too complicated and a bit of a rabbit hole
    # integration testing will catch the rest of the route testing, above is sufficient for a quick smoke test!!!!

    def test_process_input_file_input(self):
        # 'src/tests/test_text_files/test1.txt'
        file_path = os.path.join(os.path.dirname(__file__), 'test_text_files', 'test1.txt')
        print(file_path)

        with open(file_path, 'rb') as file:
            response = self.app.post('/text-analy', data={'selected_option': 'files_input', 'file_input': [file]})
        self.assertEqual(response.status_code, 200)

    def test_process_input_files_input(self):
        file_directory = os.path.join(os.path.dirname(__file__), 'test_text_files')
        uploaded_files = []

        for filename in os.listdir(file_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(file_directory, filename)
                with open(file_path, 'rb') as file:
                    uploaded_files.append(('file_input', (file.name, file.read(), 'text/plain')))

        with self.app as client:
            ## pass the dictionary map of uploaded_files as a pointer argument
            # https://flask.palletsprojects.com/en/3.0.x/testing/#form-data
            response = client.post('/text-analy',
                                   data={'selected_option': 'files_input', **dict(uploaded_files)})

        self.assertEqual(response.status_code, 200)

    def test_select_ctv_news(self):
        response = self.app.post('/text-analy', data={'selected_option': 'news_article_sources',
                                                      'news_article_sources': '{"name": "CTV News", "url": "https://www.ctvnews.ca/rss/ctvnews-ca-top-stories-public-rss"}'})
        self.assertEqual(response.status_code, 200)

    def test_select_abc_news(self):
        response = self.app.post('/text-analy', data={'selected_option': 'news_article_sources',
                                                      'news_article_sources': '{"name": "ABC News", "url": "https://abcnews.go.com/abcnews/topstories"}'})
        self.assertEqual(response.status_code, 200)

    def test_select_al_jazeera(self):
        response = self.app.post('/text-analy', data={'selected_option': 'news_article_sources',
                                                      'news_article_sources': '{"name": "Al Jazeera", "url": "https://feeder.co/discover/9f94548972/aljazeera-com-default-html"}'})
        self.assertEqual(response.status_code, 200)

    def test_database_info_route(self):
        response = self.app.get("/database_info")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
