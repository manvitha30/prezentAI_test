import requests
import logging
import pytest
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pytest_html import extras
import responses

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_request_response(response):
    """Logs request and response details."""
    logging.info(f"Request URL: {response.request.url}")
    logging.info(f"Request Method: {response.request.method}")
    logging.info(f"Request Headers: {response.request.headers}")
    logging.info(f"Request Body: {getattr(response.request, 'body', 'No Body')}")
    logging.info(f"Response Status: {response.status_code}")
    logging.info(f"Response Body: {response.text}")

class APIAutomation:
    """
    APIAutomation class provides methods to interact with a REST API using requests.
    It includes functionalities to perform CRUD operations on posts and comments,
    implements a retry strategy for robustness, and logs request and response details.
    
    Attributes:
        BASE_URL (str): Base URL for the API endpoint.
        session (requests.Session): Session object to handle requests with retries.
    
    Methods:
        get_posts(post_id): Fetches a specific post by ID.
        get_post_comments(post_id): Retrieves comments associated with a post.
        create_post(title, body, user_id): Creates a new post with the given details.
        update_post(post_id, title, body, user_id): Updates an existing post.
        patch_post(post_id, title, body, user_id): Partially updates a post.
        delete_post(post_id): Deletes a post by ID.
        _make_request(method, url, **kwargs): Handles API requests with retry strategy.
    """
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    def __init__(self):
        """Initializes APIAutomation with retry logic and session handling."""
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
    
    def get_posts(self, post_id):
        """Fetches a post by ID."""
        url = f"{self.BASE_URL}/posts/{post_id}"
        return self._make_request("GET", url)
    
    def get_post_comments(self, post_id):
        """Fetches a post comments by ID."""
        url = f"{self.BASE_URL}/posts/{post_id}/comments"
        return self._make_request("GET", url)
    
    def create_post(self, title, body, user_id):
        """Creates a new post."""
        url = f"{self.BASE_URL}/posts"
        payload = {"title": title, "body": body, "userId": user_id}
        return self._make_request("POST", url, json=payload)
    
    def update_post(self, post_id, title, body, user_id):
        """Updates existing post."""
        url = f"{self.BASE_URL}/posts/{post_id}"
        payload = {"title": title, "body": body, "userId": user_id}
        return self._make_request("PUT", url, json=payload)

    
    def patch_post(self, post_id, title=None, body=None, user_id=None):
        """Updates existing post."""
        url = f"{self.BASE_URL}/posts/{post_id}"
        payload = {key: value for key, value in {"title": title, "body": body, "userId": user_id}.items() if value is not None}
        return self._make_request("PATCH", url, json=payload)
    
    def delete_post(self, post_id):
        """Deletes existing post."""
        url = f"{self.BASE_URL}/posts/{post_id}"
        return self._make_request("DELETE", url)
    
    def _make_request(self, method, url, **kwargs):
        """Handles HTTP requests with logging and error handling."""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error during {method} request: {http_err}")
            return response  # Return response even on 404 or 500 errors
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error during {method} request: {req_err}")
            mock_response = requests.Response()
            mock_response.status_code = 500  # Simulate server failure response
            return mock_response  # Return mock response instead of None


@pytest.mark.parametrize("post_id", [1, 2, 3, -1, "abc", 9999])
def test_get_posts(post_id):
    api = APIAutomation()
    response = api.get_posts(post_id)

    assert response is not None, f"Expected a response for post_id={post_id}, but got None"
    assert response.status_code in [200, 404, 500], f"Unexpected status code {response.status_code} for post_id={post_id}"
    
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict), f"Expected JSON response for post_id={post_id}, but got {type(data)}"
    elif response.status_code == 404:
        assert response.json() == {}, f"Expected empty JSON for post_id={post_id}, but got {response.json()}"
    elif response.status_code == 500:
        logging.warning(f"Received 500 response for post_id={post_id}")


@pytest.mark.parametrize("post_id", [1, 2, 3, -1, 9999])
def test_get_post_comments(post_id):
    api = APIAutomation()
    response = api.get_post_comments(post_id)
    
    assert response is not None, "Response should not be None"  # FIXED: Added None check
    assert response.status_code in [200, 404], f"Expected 200 or 404, got {response.status_code}"
    
    if response.status_code == 200 and post_id not in [-1, 9999]:
        json_data = response.json()
        assert isinstance(json_data, list) and len(json_data) > 0, "Expected non-empty list"

@pytest.mark.parametrize("title, body, user_id", [
    ("Test Title", "Test Body", 1),
    ("", "No title", 3),
    ("Valid Title", "", 4)
])
def test_create_post(title, body, user_id):
    api = APIAutomation()
    response = api.create_post(title, body, user_id)
    
    assert response is not None and response.status_code == 201
    json_data = response.json()
    assert json_data["title"] == title
    assert json_data["body"] == body
    assert json_data["userId"] == user_id
    assert "id" in json_data

@pytest.mark.parametrize("post_id, title, body, user_id", [
    (1, "Updated Title", "Updated Body", 1),
    (9999, "Non-existent", "Body", 2)
])
def test_update_post(post_id, title, body, user_id):
    api = APIAutomation()
    response = api.update_post(post_id, title, body, user_id)

    assert response is not None, f"Expected a response for post_id={post_id}, but got None"
    assert response.status_code in [200, 404, 500], f"Unexpected status code {response.status_code} for post_id={post_id}"
    
    if response.status_code == 200:
        data = response.json()
        assert data["title"] == title, "Title update failed"
        assert data["body"] == body, "Body update failed"
        assert data["userId"] == user_id, "User ID mismatch"
    elif response.status_code == 404:
        assert response.json() == {}, f"Expected empty JSON for post_id={post_id}, but got {response.json()}"
    elif response.status_code == 500:
        logging.warning(f"Received 500 response for post_id={post_id}")

@pytest.mark.parametrize("post_id", [1, 9999])
def test_delete_post(post_id):
    api = APIAutomation()
    response = api.delete_post(post_id)

    assert response is not None, "Response should not be None"
    assert response.status_code == 200, f"DELETE request returned {response.status_code}, expected 200"

@responses.activate
def test_mock_get_posts():
    responses.add(
        responses.GET, "https://jsonplaceholder.typicode.com/posts/1", 
        json={"userId": 1, "id": 1, "title": "Mock Title", "body": "Mock Body"}, 
        status=200
    )
    api = APIAutomation()
    response = api.get_posts(1)

    assert response is not None, "Mocked response should not be None"
    assert response.status_code == 200
    assert response.json()["title"] == "Mock Title"

# Pytest HTML reporting hook
def pytest_html_report_title(report):
    report.title = "API Automation Test Report"

def pytest_html_results_summary(prefix):
    prefix.extend([extras.html("<p>API Automation Report</p>")])
