import unittest
from unittest.mock import MagicMock, patch
from rest_api_client import RESTAPIClient


class TestRESTAPIClient(unittest.TestCase):

    @patch('rest_api_client.requests.Session')
    def setUp(self, mock_session):
        self.mock_session = mock_session.return_value
        self.api_client = RESTAPIClient("https://resttest10.herokuapp.com")

    def test_get_json_success(self):
        # Mock successful response
        expected_response = {'message': 'success'}
        self.mock_session.get.return_value.json.return_value = expected_response

        # Perform the get_json method
        result = self.api_client.get_json(1)

        # Assertions
        self.assertEqual(result, expected_response)
        self.mock_session.get.assert_called_once_with("https://resttest10.herokuapp.com/api/responses?serial=1")

    def test_get_json_error(self):
        # Mock an error response
        self.mock_session.get.return_value.raise_for_status.side_effect = Exception("Mocked Error")

        # Perform the get_json method
        with self.assertRaises(Exception):
            self.api_client.get_json(1)

        # Assertions
        self.mock_session.get.assert_called_once_with("https://resttest10.herokuapp.com/api/responses?serial=1")

    def test_process_json(self):
        # Mock JSON responses for processing
        json_response_1 = {'message': {'subset': {'general': {'quantities': {'first': 10, 'second': 20, 'third': 30}}}}}
        json_response_2 = {'message': {'subset': {'general': {'quantities': {'first': 5, 'second': 25, 'third': 35}}}}}

        # Perform the process_json method
        result = self.api_client.process_json(json_response_1, json_response_2)

        # Assertions
        expected_result = {
            "serial": 3,
            "message": {
                "subset": {
                    "general": {
                        "information": {
                            "date": "1-2-2021",
                            "version": "3.00"
                        },
                        "quantities": {
                            "first": 10,
                            "second": 25,
                            "third": 35
                        }
                    }
                }
            }
        }
        self.assertEqual(result, expected_result)

    def test_process_json_no_date_version(self):
        # Mock JSON responses for processing with missing date and version
        json_response_1 = {'message': {'subset': {'general': {'quantities': {'first': 10, 'second': 20, 'third': 30}}}}}
        json_response_2 = {'message': {'subset': {'general': {'quantities': {'first': 5, 'second': 25, 'third': 35}}}}}

        # Remove date and version from json_response_1
        json_response_1['message']['subset']['general'].pop('information', None)

        # Perform the process_json method
        result = self.api_client.process_json(json_response_1, json_response_2)

        # Assertions
        expected_result = {
            "serial": 3,
            "message": {
                "subset": {
                    "general": {
                        "information": {
                            "date": "1-2-2021",  # Default date
                            "version": "3.00"  # Default version
                        },
                        "quantities": {
                            "first": 10,
                            "second": 25,
                            "third": 35
                        }
                    }
                }
            }
        }
        self.assertEqual(result, expected_result)

    def test_send_processed_json_success(self):
        # Mock successful response
        self.mock_session.post.return_value.raise_for_status.return_value = None

        # Perform the send_processed_json method
        result = self.api_client.send_processed_json({"serial": 3, "message": {"subset": {"general": {}}}})

        # Assertions
        self.assertIsNone(result)
        self.mock_session.post.assert_called_once_with("https://resttest10.herokuapp.com/api/process", json={"serial": 3, "message": {"subset": {"general": {}}}})

    def test_send_processed_json_error(self):
        # Mock an error response
        self.mock_session.post.return_value.raise_for_status.side_effect = Exception("Mocked Error")

        # Perform the send_processed_json method
        with self.assertRaises(Exception):
            self.api_client.send_processed_json({"serial": 3, "message": {"subset": {"general": {}}}})

        # Assertions
        self.mock_session.post.assert_called_once_with("https://resttest10.herokuapp.com/api/process", json={"serial": 3, "message": {"subset": {"general": {}}}})


if __name__ == '__main__':
    unittest.main()
