#login_page.py

import logging
from seleniumbase import BaseCase
from utils.logger_util import Logger
from config import USERNAME, PASSWORD, URL

class LoginPage:
    """
    A Page Object Model (POM) class for the Login Page.
    
    This class handles user login, logout, and login validation using SeleniumBase framework.
    """
    def __init__(self, test: BaseCase, username=USERNAME, password=PASSWORD):
        """
        Initializes the LoginPage with SeleniumBase test instance.

        Args:
            test (BaseCase): Instance of SeleniumBase test case.
            username (str, optional): User's email/username. Defaults to USERNAME from config.
            password (str, optional): User's password. Defaults to PASSWORD from config.
        """
        self.test = test
        self.url = URL
        self.username = username
        self.password = password
        
        self.logger = Logger().get_logger()  # Use the singleton logger

        # Locators
        self.email_field = "input#username"  # Email input field
        self.continue_button = "button#continue"  # Continue button
        self.password_field = "input#password"  # Password input field
        self.login_button = "button#submit"  # Login button
        self.dashboard_element = "span[data-v-194b5dfe]"  # Element visible after login
        self.profile_icon = "div.profile-user-avatar"  # Profile icon for logout
        self.logout_button = "button.log-out-button"  # Logout button


    def login(self):
        """
        Handles the login process with necessary validations.

        Steps:
        1. Open the login page.
        2. Enter the email and click 'Continue'.
        3. Enter the password and click 'Login'.
        4. Verify successful login.

        Raises:
            Exception: If login fails, an error is logged and a screenshot is taken.
        """
        try:
            self.logger.info("Opening login page: %s", self.url)

            self.test.open(self.url)
            self.test.wait_for_element_visible(self.email_field, timeout=10)
            self.test.assert_element(self.email_field,  by="css selector", timeout=10)

            # Step 1: Enter Email & Click Continue
            self.logger.info("Entering username: %s", self.username)
            self.test.type(self.email_field, self.username)
            self.test.wait(1)  # Ensure the input event triggers

            # Check if the Continue button is enabled
            self.logger.info("Clicking 'Continue' button")
            assert self.test.is_element_enabled(self.continue_button), "Continue button is not enabled!"
            self.test.click(self.continue_button)


            # Step 2: Wait for Password Field & Enter Password
            self.test.wait_for_element_visible(self.password_field, timeout=5)
            self.logger.info("Entering password")
            self.test.assert_element(self.password_field, by="css selector", timeout=10)
            self.test.type(self.password_field, self.password)

            # Check if the Log in button is enabled
            assert self.test.is_element_enabled(self.login_button), "Login button is not enabled!"
            self.logger.info("Clicking 'Login' button")
            self.test.click(self.login_button)

            # Step 3: Verify Successful Login
            self.test.wait_for_element_visible(self.dashboard_element, timeout=20)
            self.test.assert_element(self.dashboard_element, by="css selector", timeout=10)
            self.logger.info("Login successful!")
        except Exception as e:
            self.logger.error("Login failed! Error: %s", e)
            self.test.save_screenshot("logs/login_failure.png")  # Captures a screenshot for debugging
            raise

    def is_login_successful(self):
        """
        Verifies login success by checking if the dashboard is visible.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        success = self.test.is_element_visible(self.dashboard_element)
        self.logger.info("Login success check: %s", success)
        return success

    def logout(self):
        """
        Logs out from the application and verifies successful logout.

        Steps:
        1. Click on the profile icon.
        2. Click on the logout button.
        3. Verify that the email field is visible again.

        Raises:
            Exception: If logout fails, an error is logged and a screenshot is taken.
        """
        try:
            self.logger.info("Logging out...")
            self.test.click(self.profile_icon)
            self.test.wait_for_element_visible(self.logout_button, timeout=5)
            self.test.assert_element(self.logout_button, by="css selector", timeout=10)
            self.test.click(self.logout_button)

            # Verify user is logged out
            self.test.wait_for_element_visible(self.email_field, timeout=10)  
            self.test.assert_element(self.email_field, by="css selector", timeout=10)
            self.logger.info("Logout successful!")
        except Exception as e:
            self.logger.error("Logout failed! Error: %s", e)
            self.test.save_screenshot("logs/logout_failure.png")
            raise