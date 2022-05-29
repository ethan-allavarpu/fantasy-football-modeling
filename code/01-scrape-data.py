import pandas as pd
from selenium import webdriver
import time

def scrape_ff_yr(years: list, directory: str = ''):
    '''
    scrape_ff_yr(years: list, directory: str = '')

    Scrape fantasy football statistics from Pro Football Reference for provided years.
    Provided the outputs as CSV files and as a list of data frames for each year.

    Parameters
    ----------
    years: list
        The fantasy football years for which to gather data from Pro Football Reference
    directory: str, default = ''
        The directory used to write CSV files. Defaults to parent directory ('')

    Returns
    -------
    data_tables: list
        A list of the tabular data tables from Pro Football Reference for the given years.
        One element for each year (in the provided order)

    Notes
    -----
    This function uses the Firefox webdriver from Selenium. To implement this, geckodriver must be installed and in your bin
    This function also returns CSV files for each year in the given directory
    '''

    data_tables = []
    driver = webdriver.Firefox()
    for year in years:
        url_path = 'https://www.pro-football-reference.com/years/' + str(year) + '/fantasy.htm'
        driver.get(url_path)
        time.sleep(0.5)
        table_html = driver.find_element_by_xpath('//*[@id="fantasy"]').get_attribute('outerHTML')
        data_table = pd.read_html(table_html)[0]
        file_name = directory + 'ff_' + str(year) + '.csv'
        data_table.to_csv(file_name)
        data_tables.append(data_table)
        time.sleep(0.5)
    driver.quit()
    return data_tables

ff_years = [*range(1991, 2022)]
ff_data = scrape_ff_yr(years = ff_years, directory = 'data/raw/')