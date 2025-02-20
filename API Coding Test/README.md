# API Automation with Python and Requests

## Overview
This project provides an automated test suite for REST API endpoints using Python's `requests` module. It supports CRUD operations on posts and comments using `jsonplaceholder.typicode.com`, a mock API.

## Features
- Supports GET, POST, PUT, PATCH, and DELETE operations
- Implements retry mechanisms for robustness
- Logs API request and response details
- Uses `pytest` for test automation with parameterization and mocking
- Generates HTML reports using `pytest-html`

## Prerequisites
Ensure you have Python 3 installed. You can verify your installation using:
```sh
python --version
```

## Installation
1. Clone this repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run API tests using pytest:
```sh
pytest --html=report.html --self-contained-html
```
This generates an HTML report `report.html` with test results.

## Test Cases
- `test_get_posts`: Retrieves a specific post by ID.
- `test_get_post_comments`: Retrieves comments associated with a post.
- `test_create_post`: Creates a new post.
- `test_update_post`: Updates an existing post.
- `test_patch_post`: Partially updates a post.
- `test_delete_post`: Deletes a post.

## Mocking API Responses
The test suite includes mocked responses using the `responses` library to simulate API behavior for unit testing.

## Logging
All requests and responses are logged to ensure traceability and debugging support.

