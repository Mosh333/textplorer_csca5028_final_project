import os
import unittest
from unittest.mock import patch
from uuid import UUID

from src.models.database import insert_analysis_results, fetch_database_info


# Must set the following environment variables in the test run or it will fail!!!
# set AWS_ACCESS_KEY_ID=...
# set AWS_SECRET_ACCESS_KEY=...
# set AWS_REGION=us-east-1
# set DYNAMODB_TABLE_NAME=textplorer-nosql-db
class TestDatabase(unittest.TestCase):

    # Will skip actual unit tests for sake of saving DB read and write costs
    @patch("src.models.database.table.put_item")
    def test_insert_analysis_results(self, mock_put_item):
        analysis_results = {
            "word_count": 100,
            "num_sentences": 5,
            "sentiment": "positive"
        }
        # random UUID data I hardcoded below
        input_requestid = UUID('123c4567-b69b-12d3-a456-123456784000')
        insert_analysis_results(analysis_results, input_requestid)
        mock_put_item.assert_called_once_with(Item=analysis_results)

    @patch("src.models.database.table.scan")
    def test_fetch_database_info(self, mock_scan):
        mock_scan.return_value = {'Count': 200}  # Update the return value to match the actual result
        result = fetch_database_info()
        self.assertTrue(result['total_rows_data'] > 0)  # Assert that total_rows_data is greater than 0


if __name__ == '__main__':
    unittest.main()
