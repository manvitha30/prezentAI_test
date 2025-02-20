from seleniumbase import BaseCase
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.templates_page import TemplatesPage
from utils.logger_util import Logger  

class TestTemplates(BaseCase):
    """
    Test Suite for verifying the Templates functionality.
    """

    def setUp(self):
        """
        Setup before each test case runs.
        
        Initializes:
        - Logger (logs stored in "logs/test_templates_TIMESTAMP/")
        - SeleniumBase setup for the test case.
        """
        super().setUp()
        # Initialize Logger (subdir will be "logs/test_templates_TIMESTAMP/")
        self.logger = Logger().get_logger()


    def test_template_listing(self):
        """
        Test Case: Verify Template Listing
        
        Steps:
        1. Log in to the application.
        2. Navigate to the Templates tab.
        3. Fetch and log the first five templates in alphabetical order.
        4. Fetch and log the active template.
        5. Log out and verify successful logout.

        Assertions:
        - Login should be successful.
        - Templates page should load correctly.
        - Logout should return to the login page.
        """
        self.logger.info("Starting Test: Template Listing")

        try:
            # Initialize Page Objects
            login_page = LoginPage(self)
            dashboard = DashboardPage(self)
            templates_page = TemplatesPage(self)

            # Step 1: Login
            self.logger.info("Attempting to log in...")
            login_page.login()
            assert login_page.is_login_successful(), "Login failed!"
            self.logger.info("Login successful.")

            # Step 2: Navigate to Templates
            self.logger.info("Navigating to Templates tab...")
            dashboard.go_to_templates()
            templates_page.verify_templates_page_loaded()
            self.logger.info("Templates page loaded successfully.")

            # Step 3: Get and print the first five templates
            self.logger.info("Fetching first five templates in alphabetical order...")
            templates_page.get_templates_list()
            self.logger.info("First 5 Template names have been logged.")

            # Step 4: Get and print the active template
            self.logger.info("Fetching active template...")
            templates_page.get_active_template()

            # Step 5: Logout
            self.logger.info("Logging out...")
            login_page.logout()
            assert self.is_element_visible(login_page.email_field), "Logout failed!"
            self.logger.info("Logout successful.")

        except AssertionError as e:
            self.logger.error(f"Test Failed: {str(e)}")
            screenshot_path = "logs/test_template_listing_failure.png"
            self.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            raise  # Re-raise the exception to fail the test

    def tearDown(self):
        """
        Cleanup after each test case runs.
        
        Logs test execution completion and calls SeleniumBase teardown.
        """
        self.logger.info("Test execution completed.")
        super().tearDown()

## Run the test with:
## py -m pytest -s .\tests\test_templates.py --html=report.html --browser=chrome --log-path=logs/
