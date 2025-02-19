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
    logging.info(f"Request URL: {response.request.url}")
    logging.info(f"Request Method: {response.request.method}")
    logging.info(f"Request Headers: {response.request.headers}")
    logging.info(f"Request Body: {response.request.body}")
    logging.info(f"Response Status: {response.status_code}")
    logging.info(f"Response Body: {response.text}")

class APIAutomation:
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
    
    def get_posts(self, post_id=None):
        url = f"{self.BASE_URL}/posts/{post_id}" if post_id else f"{self.BASE_URL}/posts"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            log_request_response(response)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching posts: {e}")
            return None
    
    def get_post_comments(self, post_id):
        url = f"{self.BASE_URL}/posts/{post_id}/comments"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            log_request_response(response)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching post comments: {e}")
            return None
    
    def create_post(self, title, body, user_id):
        url = f"{self.BASE_URL}/posts"
        payload = {"title": title, "body": body, "userId": user_id}
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            log_request_response(response)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error creating post: {e}")
            return None

@pytest.mark.parametrize("post_id", [1, 2, 3, -1, "abc", 9999])
def test_get_posts(post_id):
    api = APIAutomation()
    response = api.get_posts(post_id)
    
    if post_id in [-1, "abc", 9999]:
        assert response is None or response.status_code == 404, f"Expected 404 for invalid ID, got {response.status_code}"
    else:
        assert response is not None, "Response should not be None"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), dict), "Response should be a dictionary"

@pytest.mark.parametrize("post_id", [1, 2, 3, -1, 9999])
def test_get_post_comments(post_id):
    api = APIAutomation()
    response = api.get_post_comments(post_id)

    assert response is not None, "Response should not be None"
    assert response.status_code in [200, 404], f"Expected 200 or 404, got {response.status_code}"
    
    if response.status_code == 200:
        if post_id in [-1, 9999]:  # Only check for empty response for invalid IDs
            assert response.json() == [], f"Expected empty response for invalid ID, got {response.json()}"
        else:  
            assert isinstance(response.json(), list), "Expected a list of comments for valid post_id"
            assert len(response.json()) > 0, "Expected non-empty response for valid post_id"


@pytest.mark.parametrize("title, body, user_id", [
    ("Test Title 1", "Test Body 1", 1),
    ("Test Title 2", "Test Body 2", 2),
    ("", "No title", 3),
    ("Valid Title", "", 4)
])
def test_create_post(title, body, user_id):
    api = APIAutomation()
    response = api.create_post(title, body, user_id)
    
    assert response is not None, "Response should not be None"
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert isinstance(response.json(), dict), "Response should be a dictionary"
    
    response_json = response.json()
    assert response_json["title"] == title, "Title should match"
    assert response_json["body"] == body, "Body should match"
    assert response_json["userId"] == user_id, "User ID should match"
    assert "id" in response_json, "Response should contain 'id' field"

@responses.activate
def test_mock_get_posts():
    responses.add(responses.GET, "https://jsonplaceholder.typicode.com/posts/1", 
                  json={"userId": 1, "id": 1, "title": "Mock Title", "body": "Mock Body"}, 
                  status=200)
    
    api = APIAutomation()
    response = api.get_posts(1)
    assert response.status_code == 200
    assert response.json()["title"] == "Mock Title"

# Pytest HTML reporting hook
def pytest_html_report_title(report):
    report.title = "API Automation Test Report"

def pytest_html_results_summary(prefix):
    prefix.extend([extras.html("<p>API Automation Report</p>")])
