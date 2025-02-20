# Selenium Tests

This folder contains the Selenium-based UI automation tests for the PrezentAI coding assessment. The tests are written using Python and SeleniumBase.

## Test Scenarios
The automation covers the following scenarios:
1. **Templates Page**: Print the first five templates in alphabetical order, identify the active template, and log out.
2. **Slide Library**: Add the second slide to favorites, verify it is favorited, and log out.
3. **Auto Generator**: Select the third suggested example, generate a slide, add it to favorites, download it, and log out.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Chrome & ChromeDriver
- Virtual environment (recommended)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running Tests
Execute the Selenium test suite using:
```bash
pytest -s --html=selenium_report.html --browser=chrome
```

## Reporting
After execution, an HTML report (`selenium_report.html`) will be generated, providing a summary of test results.

For any queries, reach out to Manvitha Reddy (Repo Owner).

