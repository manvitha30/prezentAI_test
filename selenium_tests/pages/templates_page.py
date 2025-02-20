#template_page.py

from seleniumbase import BaseCase
from utils.logger_util import Logger

class TemplatesPage:
    def __init__(self, test: BaseCase):
        """Initialize the TemplatesPage with SeleniumBase test instance"""
        self.test = test
        self.logger = Logger().get_logger()  # Use the singleton logger

        # Locators
        self.templates_header = "div.pt-header__title"  # Templates section title
        self.template_list = "//div[@class='pt-list__item pt-card pt-list__item v-card v-sheet theme--light']"  # Template elements
        self.active_template_name = "(//div[@class='pt-list__item pt-card pt-list__item v-card v-sheet theme--light'])[1]/div[2]/descendant::*[3]"

    def verify_templates_page_loaded(self):
        """Checks if Templates section is visible with assertions and logging"""
        try:
            self.logger.info("Verifying Templates page is loaded")
            self.test.wait_for_element_visible(self.templates_header, timeout=10)
            assert self.test.get_text(self.templates_header).strip() == "Templates", "Templates page header mismatch"
            self.logger.info("Templates page successfully loaded")
        except Exception as e:
            self.logger.error("Error verifying Templates page: %s", e)
            self.test.save_screenshot("logs/templates_page_load_failure.png")
            raise


    def get_templates_list(self):
        """Fetches the first five templates, sorts them alphabetically, and logs them"""
        try:
            self.logger.info("Fetching list of first five templates")

            templates = self.test.find_elements(self.template_list)
            assert templates, "No templates found on the page"

            template_names = []

            for i in range(min(5, len(templates))):  
                ele_xpath = f"(//div[@class='pt-list__item pt-card pt-list__item v-card v-sheet theme--light'])[{i+1}]/div[2]/descendant::*[3]"
                ele_text = self.test.get_text(ele_xpath).strip()
                template_names.append(ele_text)

            template_names.sort()

            self.logger.info("First five templates in alphabetical order: %s", template_names)
            print("\nFirst five templates in alphabetical order:")
            for template in template_names:
                print(f"- {template}")

        except Exception as e:
            self.logger.error("Error fetching templates list: %s", e)
            self.test.save_screenshot("logs/templates_list_failure.png")
            raise

    def get_active_template(self):
        """Identifies and prints the currently active template with logging"""
        try:
            self.logger.info("Fetching the currently active template")
            assert self.test.is_element_visible(self.active_template_name), "Active template not found"

            active_template = self.test.get_text(self.active_template_name).strip()
            self.logger.info("Current active template: %s", active_template)
            print(f"\nCurrent active template: {active_template}")

        except Exception as e:
            self.logger.error("Error identifying active template: %s", e)
            self.test.save_screenshot("logs/active_template_failure.png")
            raise