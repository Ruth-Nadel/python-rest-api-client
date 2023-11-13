from rest_api_client import RESTAPIClient
import json


def main(url="https://resttest10.herokuapp.com"):
    # Create an instance of the RESTAPIClient
    api_client = RESTAPIClient(url)

    # Step 1: Receive JSON by making two API calls
    json_response_1 = api_client.get_json(1)
    print("JSON Response for Serial=1:", json.dumps(json_response_1, indent=2, end="\n\n"))
    json_response_2 = api_client.get_json(2)
    print("JSON Response for Serial=2:", json.dumps(json_response_2, indent=2, end="\n\n"))

    # Step 2: Process JSON
    processed_data = api_client.process_json(json_response_1, json_response_2)

    # Step 3: Send processed JSON
    response = api_client.send_processed_json(processed_data)

    # Check if the processing was successful
    assert response.status_code == 200, f"Error in processing. Status Code: {response.status_code}. Response: {response.text}"
    assert response.json() == "correct", f"Processing was not successful. Response: {response.json()}"

    print("Processing successful. Message: correct")


if __name__ == "__main__":
    main()
