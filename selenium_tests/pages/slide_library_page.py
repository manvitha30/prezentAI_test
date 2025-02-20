#slide_library_page.py

from seleniumbase import BaseCase
from utils.logger_util import Logger

class SlideLibraryPage:
    """
    A Page Object Model (POM) class for the Slide Library Page.

    This class provides methods to interact with the Slide Library, such as verifying page load,
    adding slides to favorites, and asserting that slides have been favorited successfully.
    """
    def __init__(self, test: BaseCase):
        """
        Initializes the SlideLibraryPage with SeleniumBase test instance.

        Args:
            test (BaseCase): Instance of SeleniumBase test case.
        """
        self.test = test

        self.logger = Logger().get_logger()  # Use the singleton logger

        # Locators
        self.search_bar = "input#slide-library-search"
        self.all_slides_locator = "(//div[contains(@class, 'slide-wrapper')])"
        self.unfavorited_heart_locator = "(//div[contains(@class, 'slide-wrapper')])[{index}]/descendant::*[2]/div[3]/div[1]/descendant::*[7]"
        self.favorited_heart_locator = "(//button[contains(@class, 'mdi-heart') and contains(@class, 'primary--text')])"

    def verify_slide_library_loaded(self):
        """
        Verifies if the Slide Library page has successfully loaded.

        Steps:
        1. Wait for the search bar to be visible.
        2. Assert that the search bar is present.

        Raises:
            Exception: If the Slide Library page fails to load.
        """
        try:
            self.logger.info("Verifying Slide Library page is loaded")
            self.test.wait_for_element_visible(self.search_bar, timeout=10)
            assert self.test.is_element_visible(self.search_bar), "Slide Library search bar not found!"
            self.logger.info("Slide Library page loaded successfully")

        except Exception as e:
            self.logger.error("Error verifying Slide Library page: %s", e)
            self.test.save_screenshot("logs/slide_library_load_failure.png")
            raise

    def add_slide_to_favorites(self, slide_index):
        """
        Adds a slide to favorites by clicking the heart icon.

        Args:
            slide_index (int): The index of the slide to be favorited.

        Steps:
        1. Ensure the slide elements are loaded.
        2. Click on the heart button of the specified slide.
        3. Wait for the UI to update.

        Raises:
            Exception: If adding the slide to favorites fails.
        """
        try:
            self.logger.info("Adding slide %d to favorites", slide_index)

            # Ensure slides are loaded
            self.test.wait_for_element_visible(self.all_slides_locator, timeout=10)
            slides = self.test.find_elements(self.all_slides_locator)
            assert len(slides) >= slide_index, f"Slide index {slide_index} out of range!"

            heart_button = self.unfavorited_heart_locator.format(index=slide_index)
            self.test.click(heart_button)
            self.test.sleep(2)  # Allow time for the UI update

            self.logger.info("Successfully clicked on Favorite button for slide %d", slide_index)

        except Exception as e:
            self.logger.error("Error adding slide %d to favorites: %s", slide_index, e)
            self.test.save_screenshot("logs/add_favorite_failure.png")
            raise

    def assert_slide_favorited(self, slide_index=2):
        """
        Asserts that a slide has been successfully favorited.

        Args:
            slide_index (int, optional): The index of the slide to verify. Defaults to 2.

        Steps:
        1. Wait for the favorited heart icon to be visible.
        2. Assert that the heart icon is present, confirming the slide is favorited.

        Raises:
            Exception: If the slide is not marked as favorited.
        """
        try:
            self.logger.info("Asserting slide %d is favorited", slide_index)

            self.test.wait_for_element_visible(self.favorited_heart_locator, timeout=5)
            assert self.test.is_element_visible(self.favorited_heart_locator), f"Slide {slide_index} is not favorited!"
            
            self.logger.info("Slide %d has been successfully favorited", slide_index)
            print(f"Slide {slide_index} has been favorited successfully.")

        except Exception as e:
            self.logger.error("Assertion failed for slide %d: %s", slide_index, e)
            self.test.save_screenshot("logs/assert_favorite_failure.png")
            raise
