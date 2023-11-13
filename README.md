# REST API Client

This Python script serves as a REST API client for interacting with a remote server. It is designed to make two API calls, process the JSON responses, and send a processed JSON to the server.

## Getting Started

### Prerequisites

Make sure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/).

### Installation

Clone the repository:

```bash
git clone https://github.com/Ruth-Nadel/python-rest-api-client.git
cd rest-api-client
```

Install the required Python libraries:

```bash
pip install requests json urllib3
```

## Usage

1. Open the `rest_client.py` file.
2. Modify the `base_url` variable with the appropriate REST server address.
3. Run the script:

```bash
python rest_client.py
```

The script will make two API calls, process the JSON responses, and send a processed JSON to the server.

## Configuration

You can customize the script by adjusting the `base_url` variable and other parameters in the `rest_client.py` file.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
