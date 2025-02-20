#auto_generator_page.py

import os
from seleniumbase import BaseCase
from utils.logger_util import Logger

class AutoGeneratorPage:
    """
    A Page Object Model (POM) class for the Auto Generator Page.

    This class provides methods to interact with the Auto Generator, including selecting suggestions,
    generating slides, adding slides to favorites, and downloading slides.
    """
    def __init__(self, test: BaseCase, file_name):
        """
        Initializes the AutoGeneratorPage with SeleniumBase test instance.

        Args:
            test (BaseCase): Instance of SeleniumBase test case.
            file_name (str): Name of the file for download/favorites.
        """
        self.test = test
        self.file_name = file_name
        self.logger = Logger().get_logger()  # Use the singleton logger

        # Locators
        self.suggestion_box = "textarea[data-pendo-id='generate-propmt']"
        self.third_suggestion = "#generate-suggested-2"
        self.generate_button = "button[data-pendo-id='generate-btn']"
        self.generation_completion = "div.change-layout-container"
        self.favorite_button = "button#favorite"
        self.download_button = "button#download"

        # Add to Favorites Modal Elements
        self.modal_container = ".generateActionModalContainer"
        self.modal_input = "(//div[@class='v-text-field__slot'])[2]/input"
        self.modal_add_button = "button.primaryBtn"

        # Download Modal Elements
        self.download_modal_input = "(//div[@class='v-text-field__slot'])[2]/input"
        self.download_confirm_button = "//button[@data-pendo-id='download-cta']"
        self.download_option = "button#download-btn-from-list"
        self.verify_download_message = "//span[normalize-space()='Download Completed']"

    def assert_auto_generator_page_opened(self):
        """
        Asserts that the Auto Generator Page is loaded successfully.

        Steps:
        1. Wait for the suggestion box to be visible.
        2. Assert that the suggestion box is present.

        Raises:
            Exception: If the Auto Generator page fails to load.
        """
        try:
            self.logger.info("Verifying Auto Generator page is loaded")
            self.test.assert_element(self.suggestion_box, by="css selector", timeout=10)
            self.logger.info("Auto Generator page loaded successfully")
        except Exception as e:
            self.logger.error("Error verifying Auto Generator page: %s", e)
            self.test.save_screenshot("logs/auto_generator_load_failure.png")
            raise

    def select_third_suggestion(self):
        """
        Selects the 3rd suggested item from the dropdown.

        Steps:
        1. Click the suggestion box to open the dropdown.
        2. Wait for the 3rd suggestion to appear.
        3. Click the 3rd suggestion.

        Raises:
            Exception: If selecting the suggestion fails.
        """
        try:
            self.logger.info("Selecting 3rd suggestion from dropdown")
            self.test.click(self.suggestion_box)
            self.test.sleep(1)  # Allow time for dropdown
            self.test.wait_for_element_visible(self.third_suggestion, timeout=5)
            self.test.click(self.third_suggestion)
            self.logger.info("3rd suggestion selected successfully")
        except Exception as e:
            self.logger.error("Error selecting 3rd suggestion: %s", e)
            self.test.save_screenshot("logs/select_suggestion_failure.png")
            raise

    def generate_slide(self):
        """
        Generates a slide by clicking the "Generate" button and waiting for completion.

        Steps:
        1. Click the generate button.
        2. Wait for the completion element to appear.

        Raises:
            Exception: If the slide generation fails.
        """
        try:
            self.logger.info("Generating slide...")
            self.test.click(self.generate_button)
            self.test.wait_for_element_visible(self.generation_completion, timeout=999)
            assert self.test.is_element_visible(self.generation_completion), "Slide generation failed!"
            self.logger.info("Slide generated successfully")
        except Exception as e:
            self.logger.error("Error generating slide: %s", e)
            self.test.save_screenshot("logs/generate_slide_failure.png")
            raise

    def add_to_favorites(self):
        """
        Adds a generated slide to favorites, handling the modal popup.

        Steps:
        1. Click the favorite button.
        2. Wait for the modal to appear.
        3. Assert the modal is visible.
        4. Enter the slide name and confirm.

        Raises:
            Exception: If adding the slide to favorites fails.
        """
        try:
            self.logger.info("Adding slide to favorites")
            self.test.click(self.favorite_button)
            self.test.wait_for_element_visible(self.modal_container, timeout=5)

            # Assert modal is visible
            assert self.test.is_element_visible(self.modal_container), "Favorites modal not displayed!"

            # Enter slide name and confirm
            self.test.type(self.modal_input, self.file_name)
            self.test.click(self.modal_add_button)

            self.logger.info("Slide added to favorites successfully")
        except Exception as e:
            self.logger.error("Error adding slide to favorites: %s", e)
            self.test.save_screenshot("logs/add_favorite_failure.png")
            raise

    def download_slide(self):
        """
        Initiates the slide download, handling the modal popup.

        Steps:
        1. Click the download button.
        2. Wait for the download modal to appear.
        3. Assert the modal is visible.
        4. Click the download confirm button.
        5. Click the download option.
        6. Wait for the confirmation message.

        Raises:
            Exception: If downloading the slide fails.
        """
        try:
            self.logger.info("Initiating slide download")
            self.test.click(self.download_button)
            self.test.wait_for_element_visible(self.modal_container, timeout=5)

            # Assert download modal is visible
            assert self.test.is_element_visible(self.modal_container), "Download modal not displayed!"

            # Enter presentation name
            #self.test.type(self.download_modal_input, self.file_name)
            self.test.click(self.download_confirm_button)

            # Click download option
            self.test.click(self.download_option)
            self.test.wait_for_element_visible(self.verify_download_message, timeout=15)

        except Exception as e:
            self.logger.error("Error downloading slide: %s", e)
            self.test.save_screenshot("logs/download_failure.png")
            raise

    def verify_download(self):
        """
        Verifies that the downloaded file exists in the default downloads folder.

        Steps:
        1. Assert that the expected downloaded file exists.

        Raises:
            Exception: If the downloaded file is not found.
        """
        self.test.assert_downloaded_file(self.file_name+".pptx")
        self.logger.info(f"Download verified: {self.file_name+".pptx"}")
