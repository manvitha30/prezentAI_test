import logging
from seleniumbase import BaseCase
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.auto_generator_page import AutoGeneratorPage
from utils.logger_util import Logger  # Reusable logger

class TestAutoGenerator(BaseCase):
    """
    Test Suite for verifying the Auto Generator workflow.
    """

    def setUp(self):
        """
        Setup before each test case runs.

        Initializes:
        - Logger (logs stored in "logs/test_auto_generator_TIMESTAMP/")
        - SeleniumBase setup for the test case.
        """
        super().setUp()
        self.logger = Logger().get_logger()

    def test_auto_generator_workflow(self):
        """
        Test Case: Auto Generator Workflow

        Steps:
        1. Log in to the application.
        2. Navigate to Auto Generator page and verify it is opened.
        3. Select the third suggested slide.
        4. Generate the slide.
        5. Add the generated slide to favorites.
        6. Download the slide and verify download success.
        7. Log out from the application.

        Assertions:
        - Login should be successful.
        - Auto Generator page should load correctly.
        - The third suggested slide should be selectable.
        - The slide should generate successfully.
        - The slide should be favorited successfully.
        - The slide should download successfully.
        - Logout should return to the login page.
        """
        self.logger.info("Starting Test: Auto Generator Workflow")
        file_name = "My_Slide"

        try:
            # Initialize Page Objects
            login_page = LoginPage(self)
            dashboard = DashboardPage(self)
            auto_generator_page = AutoGeneratorPage(self, file_name)

            # Step 1: Log in
            self.logger.info("Attempting to log in...")
            login_page.login()
            assert login_page.is_login_successful(), "Login failed!"
            self.logger.info("Login successful.")

            # Step 2: Navigate to Auto Generator Page
            self.logger.info("Navigating to Auto Generator page...")
            dashboard.go_to_auto_generator()
            auto_generator_page.assert_auto_generator_page_opened()
            self.logger.info("Auto Generator page opened successfully.")

            # Step 3: Select the third suggested slide
            self.logger.info("Selecting the third suggested slide...")
            auto_generator_page.select_third_suggestion()
            self.logger.info("Third suggestion selected.")

            # Step 4: Generate the slide
            self.logger.info("Generating the slide...")
            auto_generator_page.generate_slide()
            self.logger.info("Slide generated successfully.")

            # Step 5: Add generated slide to favorites
            self.logger.info("Adding generated slide to favorites...")
            auto_generator_page.add_to_favorites()
            self.logger.info("Slide added to favorites.")

            # Step 6: Download the slide
            self.logger.info(f"Downloading the slide as '{file_name}'...")
            auto_generator_page.download_slide()

            # Step 6.1: Verify Download
            self.logger.info("Verifying downloaded file...")
            auto_generator_page.verify_download()
            self.logger.info("Download verified successfully.")

            # Step 7: Log out
            self.logger.info("Logging out...")
            login_page.logout()
            assert self.is_element_visible(login_page.email_field), "Logout failed!"
            self.logger.info("Logout successful.")

        except AssertionError as e:
            self.logger.error(f"Test Failed: {str(e)}")
            screenshot_path = "logs/test_auto_generator_failure.png"
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

# Run the test with:
# pytest -s tests/test_auto_generator.py --html=report.html --browser=chrome --log-path=logs/
