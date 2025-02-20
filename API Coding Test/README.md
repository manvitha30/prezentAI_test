# API Coding Test

This folder contains the API automation tests for the PrezentAI coding assessment. The tests validate various REST API endpoints using the `requests` module and `pytest`.

## API Details
The tests are performed on `https://jsonplaceholder.typicode.com/`, a mock API.

### Supported Endpoints:
- `GET /posts`
- `GET /posts/{id}`
- `GET /posts/{id}/comments`
- `POST /posts`
- `PUT /posts/{id}`
- `PATCH /posts/{id}`
- `DELETE /posts/{id}`

## Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running Tests
Execute the API test suite using:
```bash
pytest --html=api_report.html
```

## Reporting
After execution, an HTML report (`api_report.html`) will be generated, providing a summary of test results.

For any queries, reach out to Manvitha Reddy (Repo Owner).

