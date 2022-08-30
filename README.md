# fantasy-football-modeling
Advanced machine learning models to predict future fantasy football performance. T::under-construction::

Before implementation, ensure that you have [geckodriver](https://github.com/mozilla/geckodriver/releases) installed and make sure it is in your bin path to use Selenium Webdriver. Geckodriver uses the Firefox browser; if you prefer an alternate browser implementation, you can adjust the code accordingly to scrape the data correctly.

---
## Model Deployment
Before running any code files, you will need to follow these steps:
1. Install (geckodriver)[https://github.com/mozilla/geckodriver/releases] and make sure it is in your bin path for Selenium Webdriver
2. Run `pip install -r package-reqs.txt` in Terminal/Command Line Interface to install the required packages in `package-reqs.txt`

Code scripts/notebooks should be run in numerical order by the number at the start of each file
  - e.g., `01-.\*.py`, `02-.\*.py`, etc.
  - Files with the same initial digits can be run simultaneously or in any order
  
Alternatively, you can use the Shell script `model-cli.sh` to have the entire model (including the scraping process) run in a single file. This also downloads the required packages in `package-reqs.txt`.

---

Data collected from Pro Football Reference (e.g., https://www.pro-football-reference.com/years/2021/fantasy.htm)
