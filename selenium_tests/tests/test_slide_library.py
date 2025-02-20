import logging
from seleniumbase import BaseCase
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.slide_library_page import SlideLibraryPage
from utils.logger_util import Logger  # Reusable logger

class TestSlideLibrary(BaseCase):
    """
    Test Suite for verifying the Slide Library functionality.
    """
    def setUp(self):
        """
        Setup before each test case runs.
        
        Initializes:
        - Logger (logs stored in "logs/test_slide_library_TIMESTAMP/")
        - SeleniumBase setup for the test case.
        """
        super().setUp()
        self.logger = Logger().get_logger()

    def test_add_slide_to_favorites(self):
        """
        Test Case: Add Slide to Favorites

        Steps:
        1. Log in to the application.
        2. Navigate to Slide Library.
        3. Verify Slide Library is loaded.
        4. Add the 2nd slide to Favorites.
        5. Verify the slide is favorited.
        6. Log out from the application.

        Assertions:
        - Login should be successful.
        - Slide Library should load correctly.
        - The slide should be favorited successfully.
        - Logout should return to the login page.
        """
        self.logger.info("Starting Test: Add Slide to Favorites")

        try:
            # Initialize Page Objects
            login_page = LoginPage(self)
            dashboard = DashboardPage(self)
            slide_library = SlideLibraryPage(self)

            # Step 1: Login
            self.logger.info("Attempting to log in...")
            login_page.login()
            assert login_page.is_login_successful(), "Login failed!"
            self.logger.info("Login successful.")

            # Step 2: Navigate to Slide Library
            self.logger.info("Navigating to Slide Library...")
            dashboard.go_to_slide_library()

            # Step 3: Verify Slide Library is Loaded
            self.logger.info("Verifying Slide Library is loaded...")
            slide_library.verify_slide_library_loaded()
            self.logger.info("Slide Library loaded successfully.")

            # Step 4: Add 2nd Slide to Favorites
            self.logger.info("Adding the 2nd slide to favorites...")
            slide_library.add_slide_to_favorites(slide_index=2)  #adding 2nd slide to favorites 
            self.logger.info("Slide added to favorites.")

            # Step 5: Assert Slide is Favorited
            self.logger.info("Verifying slide is favorited...")
            slide_library.assert_slide_favorited()
            self.logger.info("Slide successfully favorited.")

            # Step 6: Logout
            self.logger.info("Logging out...")
            login_page.logout()
            assert self.is_element_visible(login_page.email_field), "Logout failed!"
            self.logger.info("Logout successful.")

        except AssertionError as e:
            self.logger.error(f"Test Failed: {str(e)}")
            screenshot_path = "logs/test_add_slide_to_favorites_failure.png"
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
## py -m pytest -s .\tests\test_slide_library.py --html=report.html --browser=chrome --log-path=logs/
