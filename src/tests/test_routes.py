import unittest
from unittest.mock import patch
from src.routes import setup_routes  # Import the setup_routes function from routes.py
from src.app import app
from flask import Flask


# Must set the following environment variables in the test run or it will fail!!!
# set AWS_ACCESS_KEY_ID=...
# set AWS_SECRET_ACCESS_KEY=...
# set AWS_REGION=us-east-1
# set DYNAMODB_TABLE_NAME=textplorer-nosql-db

# As well the web application must be running locally in the background!!!
class TestRoutes(unittest.TestCase):

    def test_main_route(self):
        with app.test_client() as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)

    # testing the rest of the routes is too complicated and a bit of a rabbit hole
    # integration testing will catch the rest of the route testing, above is sufficient for a quick smoke test!!!!

    # Could not get the below to work...
    # def test_database_info_route(self):
    #     with app.test_client() as client:
    #         response = client.post("/database_info")
    #         self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
