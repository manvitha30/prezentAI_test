# Prezent.ai QA Automation Coding Test

## Overview
This repository contains an automated test suite for a coding assessment as part of the hiring process for a **Lead QA Engineer** position at Prezent.ai. The tests are written in **Python** using the **SeleniumBase** framework, following an **object-oriented design** with reusable components.

## Tech Stack
- **Programming Language**: Python
- **Testing Framework**: SeleniumBase
- **Logging**: Python logging module
- **Reporting**: Pytest HTML reports
- **Assertions**: SeleniumBase assertion methods

## Project Structure
```
prezentAI_test/
│-- pages/               # Page Object Models (POM) for different sections of the app
│   │-- login_page.py
│   │-- dashboard_page.py
│   │-- templates_page.py
│   │-- slide_library_page.py
│   │-- auto_generator_page.py
│
│-- tests/               # Test cases for the assigned tasks
│   │-- test_templates.py
│   │-- test_slide_library.py
│   │-- test_auto_generator.py
│
│-- utils/               # Utility classes (e.g., logging)
│   │-- logger_util.py
│
│-- requirements.txt     # Dependencies required to run the tests
│-- README.md            # Documentation
```

## Test Cases
The following test cases are automated:

### 1. **Template Listing Test**
**File:** `test_templates.py`
- Logs into the application.
- Navigates to the **Templates** tab.
- Prints the first five templates in alphabetical order.
- Identifies and prints the active template.
- Logs out of the application.

### 2. **Slide Library Test**
**File:** `test_slide_library.py`
- Logs into the application.
- Navigates to the **Slide Library**.
- Adds the second slide to **Favorites**.
- Asserts that the slide has been favorited.
- Logs out of the application.

### 3. **Auto Generator Workflow Test**
**File:** `test_auto_generator.py`
- Logs into the application.
- Navigates to **Auto Generator**.
- Selects the third suggested slide from the dropdown.
- Generates the slide and waits for completion.
- Adds the generated slide to **Favorites**.
- Downloads the slide and verifies the downloaded file.
- Logs out of the application.

## Setup & Execution

### Prerequisites
- Install **Python 3.8+**.
- Install dependencies using:
  ```sh
  pip install -r requirements.txt
  ```

### Running the Tests
Execute all tests using:
```sh
pytest --html=report.html --browser=chrome --log-path=logs/
```
Run individual tests:
```sh
pytest tests/test_templates.py --html=report.html --browser=chrome
pytest tests/test_slide_library.py --html=report.html --browser=chrome
pytest tests/test_auto_generator.py --html=report.html --browser=chrome
```

## Reporting & Logs
- **HTML Reports**: Generated after each test run (`report.html`).
- **Logs**: Stored in `logs/` folder, containing execution details and failure screenshots.

## GitHub Repository
[GitHub Repo](https://github.com/manvitha30/prezentAI_test)

## Notes
- The framework follows the **Page Object Model (POM)** for maintainability.
- Logging is centralized for better debugging and issue tracking.
- The test suite is designed to be **scalable and reusable** for future enhancements.

---
*For any issues, please feel free to reach out.*

