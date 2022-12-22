# fantasy-football-modeling
Advanced machine learning models to predict future fantasy football performance.

🚧 This repository is currently being developed. Last updated on September 1, 2022

Before implementation, ensure that you have [geckodriver](https://github.com/mozilla/geckodriver/releases) installed and make sure it is in your bin path to use Selenium Webdriver. Geckodriver uses the Firefox browser; if you prefer an alternate browser implementation, you can adjust the code accordingly to scrape the data correctly.

## Model Deployment
There are two options for how to execute the model: a single Shell script (simpler option) or a Python script-by-script implementation.

### Command-Line Interface
`model-cli.sh` is a command-line Shell script to run the entire model (including the scraping process) a single file. This also downloads the required packages listed in `package-reqs.txt`. You can run the Shell script with `bash model-cli.sh`

### Individual Python Files
1. Run `pip install -r package-reqs.txt` in Terminal/Command Prompt to ensure the required packages are available for use.
2. Code scripts/notebooks should be run in numerical order by the number at the start of each file.
    - e.g., `01-.\*.py`, `02-.\*.py`, etc.
    - Files with the same initial digits can be run simultaneously or in any order
  

---

Data collected from Pro Football Reference (e.g., https://www.pro-football-reference.com/years/2021/fantasy.htm)
