import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RESTAPIClient:
    def __init__(self, base_url):
        self._base_url = base_url
        self._session = self._create_session()

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @staticmethod
    def _create_session():
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]))
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.timeout = (2, 20)
        return session

    def get_json(self, serial):
        try:
            response = self.session.get(f"{self.base_url}/api/responses?serial={serial}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RetryError as retry_err:
            if "503 error responses" in str(retry_err):
                raise Exception(f"Error | Too many 503 errors occurred while fetching JSON for serial {serial}")
                # Handle the situation with too many 503 errors as needed
            else:
                raise Exception(f"Error | occurred while fetching JSON for serial {serial}: {str(retry_err)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error | occurred while fetching JSON for serial {serial}: {str(e)}")

    @staticmethod
    def process_json(json_response_1, json_response_2):
        try:
            processed_data = {
                "serial": 3,
                "message": {
                    "subset": {
                        "general": {
                            "information": {
                                "date": "1-2-2021",
                                "version": "3.00"
                            },
                            "quantities": {
                                "first": max(json_response_1["message"]["subset"]["general"]["quantities"]["first"],
                                            json_response_2["message"]["subset"]["general"]["quantities"]["first"]),
                                "second": max(json_response_1["message"]["subset"]["general"]["quantities"]["second"],
                                             json_response_2["message"]["subset"]["general"]["quantities"]["second"]),
                                "third": max(json_response_1["message"]["subset"]["general"]["quantities"]["third"],
                                            json_response_2["message"]["subset"]["general"]["quantities"]["third"])
                            }
                        }
                    }
                }
            }
            return processed_data
        except Exception as e:
            raise Exception(f"Error | occurred while processing JSON: {str(e)}")

    def send_processed_json(self, processed_data):
        try:
            response = self.session.post(f"{self.base_url}/api/process", json=processed_data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error | occurred while sending processed JSON: {str(e)}")
