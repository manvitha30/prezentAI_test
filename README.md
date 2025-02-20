# PrezentAI Coding Test

This repository contains automated test solutions for the PrezentAI coding assessment. It includes Selenium-based UI tests and API automation using Python.

## Repository Structure
```
prezentAI_test/
│-- API Coding Test/            # API automation using requests & pytest
│   │-- api_automation.py       # API automation class
│   │-- test_api.py             # API test cases using pytest
│   │-- requirements.txt        # Dependencies for API automation
│   │-- README.md               # API test setup & execution details
│
│-- selenium_tests/             # Selenium UI test automation
│   │-- pages/                   # Page Object Model classes
│   │-- tests/                   # Selenium test cases
│   │-- utils/                   # Utility functions
│   │-- requirements.txt         # Dependencies for Selenium tests
│   │-- README.md                # Selenium test setup & execution details
│
│-- README.md                    # Main project overview
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Chrome & ChromeDriver
- Virtual environment (recommended)

### Install Dependencies

#### Selenium Tests
```bash
cd selenium_tests
pip install -r requirements.txt
```

#### API Tests
```bash
cd "API Coding Test"
pip install -r requirements.txt
```

## Running Tests

### Selenium Tests
```bash
pytest --html=report.html --browser=chrome
```

### API Tests
```bash
pytest --html=api_report.html
```

## Reporting
After execution, test reports will be generated in the respective directories as HTML reports.

For any queries, reach out to Manvitha Reddy (Repo Owner).

