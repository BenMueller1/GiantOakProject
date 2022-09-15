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

    # close driver
    driver.close()







if __name__ == "__main__":
    main()