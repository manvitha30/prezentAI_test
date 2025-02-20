#dashboard_page.py
import logging
from seleniumbase import BaseCase
from utils.logger_util import Logger

class DashboardPage:
    """
    A Page Object Model (POM) class for the Dashboard Page.

    This class provides navigation methods to different sections of the dashboard,
    including Templates, Slide Library, and Auto Generator.
    """
    def __init__(self, test: BaseCase):
        """
        Initializes the DashboardPage with SeleniumBase test instance.

        Args:
            test (BaseCase): Instance of SeleniumBase test case.
        """
        self.test = test

        self.logger = Logger().get_logger()  # Use the singleton logger


        # Locators
        self.profile_icon = "div.profile-user-avatar"  # Profile icon for accessing templates
        self.templates_tab = "a#templates-tab"
        self.slide_library_tab = "div#v-step-1"
        self.auto_generator_tab = "div#v-step-3"
        
        # Unique elements that confirm page has loaded
        self.templates_section = "div.pt-header__title"
        self.slide_library_section = "input#slide-library-search"
        self.auto_generator_section = "button[data-pendo-id='generate-btn']"

    def go_to_templates(self):
        """
        Navigates to the Templates section.

        Steps:
        1. Click on the profile icon.
        2. Click on the Templates tab.
        3. Wait for the Templates section to be visible.

        Raises:
            Exception: If navigation fails, logs the error and captures a screenshot.
        """
        try:
            self.logger.info("Navigating to Templates section")
            assert self.test.is_element_visible(self.profile_icon), "Profile icon not visible"

            self.test.click(self.profile_icon)
            self.test.click(self.templates_tab)
            self.test.wait_for_element_visible(self.templates_section, timeout=10)
            assert self.test.is_element_visible(self.templates_section), "Failed to navigate to Templates"

            self.logger.info("Successfully navigated to Templates section")
        except Exception as e:
            self.logger.error("Error navigating to Templates: %s", e)
            self.test.save_screenshot("logs/templates_navigation_failure.png")
            raise


    def go_to_slide_library(self):
        """
        Navigates to the Slide Library section.

        Steps:
        1. Verify that the Slide Library tab is visible.
        2. Click on the Slide Library tab.
        3. Wait for the Slide Library section to be visible.

        Raises:
            Exception: If navigation fails, logs the error and captures a screenshot.
        """
        try:
            self.logger.info("Navigating to Slide Library section")
            assert self.test.is_element_visible(self.slide_library_tab), "Slide Library tab not visible"

            self.test.click(self.slide_library_tab)
            self.test.wait_for_element_visible(self.slide_library_section, timeout=10)
            assert self.test.is_element_visible(self.slide_library_section), "Failed to navigate to Slide Library"

            self.logger.info("Successfully navigated to Slide Library section")

        except Exception as e:
            self.logger.error("Error navigating to Slide Library: %s", e)
            self.test.save_screenshot("logs/slide_library_navigation_failure.png")
            raise

    def go_to_auto_generator(self):
        """
        Navigates to the Auto Generator section.

        Steps:
        1. Verify that the Auto Generator tab is visible.
        2. Click on the Auto Generator tab.
        3. Wait for the Auto Generator section to be visible.

        Raises:
            Exception: If navigation fails, logs the error and captures a screenshot.
        """
        try:
            self.logger.info("Navigating to Auto Generator section")
            assert self.test.is_element_visible(self.auto_generator_tab), "Auto Generator tab not visible"

            self.test.click(self.auto_generator_tab)
            self.test.wait_for_element_visible(self.auto_generator_section, timeout=10)
            assert self.test.is_element_visible(self.auto_generator_section), "Failed to navigate to Auto Generator"

            self.logger.info("Successfully navigated to Auto Generator section")

        except Exception as e:
            self.logger.error("Error navigating to Auto Generator: %s", e)
            self.test.save_screenshot("logs/auto_generator_navigation_failure.png")
            raise
