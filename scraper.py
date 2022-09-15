from os import link
import selenium
import json
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller

from time import sleep


def save_to_json_file():
    """ docstring (include params, what it does, and output) """
    pass

def convert_data_to_json():
    """ docstring (include params, what it does, and output) """
    pass

def scrape_criminal_data(criminal_link):
    """ docstring (include params, what it does, and output) """



def main():
    # install and initialize webdriver
    chromedriver_autoinstaller.install() # install and add to path
    driver = webdriver.Chrome()

    # ensure no command line arguments were passed in
    if len(sys.argv) > 1:
        sys.exit("ERROR: Please do not pass in any command line arguments")

    # open website
    driver.get("https://www.nationalcrimeagency.gov.uk/most-wanted-search")

    # accept cookies if the cookies warning pops up (if it doesn't show up, do nothing)
    sleep(2.5)   # we need to wait a few seconds for the cookies warning to show up
    accept_cookies_btn = driver.find_elements(   
        By.ID,
        "ccc-recommended-settings"
    )
    if len(accept_cookies_btn) > 0:  # find_elements will return empty list if button not found
        accept_cookies_btn[0].click()

    # open rest of page (PAGINATION)
    sleep(2.5)
    driver.find_element(
        By.XPATH, 
        "/html/body/div[@class='site-container']/div[@id='maincontent']/div[@class='row-fluid']/div[@id='content']/div[@class='span12']/div[@class='search mw-search-page']/div[@class='row-fluid']/div[@class='span9']/div[@class='pagination']/div[@class='btn btn-ncabrown load-more']"
    ).click()
    
    
    # get list of all divs containing criminals
    criminal_divs = driver.find_elements(
        By.CLASS_NAME,
        "span4"
    )

    # get links to each criminal's page
    criminal_links = []
    for div in criminal_divs:
        l = div.find_element(By.TAG_NAME, "a")
        criminal_links.append(l)

    # initialize data
    return_json = {
        "source_code": "UK_MWL",
        "source_name": " UK Most Wanted List",
        "source_url": " https://www.nationalcrimeagency.gov.uk/most-wanted-search",
        "persons": []
    }
    persons = []
    
    # scrape and record data from each criminals page
    
    for l in criminal_links:
        criminal_data = scrape_criminal_data(l)
        persons.append(criminal_data)


    # close driver
    driver.close()




if __name__ == "__main__":
    main()