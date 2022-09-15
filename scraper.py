from os import link
import selenium
import json
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller

from time import sleep

# install and initialize webdriver
chromedriver_autoinstaller.install() # install and add to path
driver = webdriver.Chrome()


def save_to_json_file():
    """ docstring (include params, what it does, and output) """
    pass

def convert_data_to_json():
    """ docstring (include params, what it does, and output) """
    pass

def click_pagination_button():
    """ docstring (include params, what it does, and output) """
    sleep(2.5)
    driver.find_element(
        By.XPATH, 
        "/html/body/div[@class='site-container']/div[@id='maincontent']/div[@class='row-fluid']/div[@id='content']/div[@class='span12']/div[@class='search mw-search-page']/div[@class='row-fluid']/div[@class='span9']/div[@class='pagination']/div[@class='btn btn-ncabrown load-more']"
    ).click()

def scrape_criminal_data(criminal_link):
    """ docstring (include params, what it does, and output) """
    # go to criminal page
    driver.get(criminal_link)  # IS THIS A RELATIVE LINK? IF SO NEED TO FIX!!
    criminal_data = {}

    # get name
    name_div = driver.find_element(By.CLASS_NAME, "page-header")
    name = name_div.find_element(By.TAG_NAME, "h2").text
    criminal_data["name"] = name

    # create about dictionary and scrape data from criminal's page
    about = {}
    about_divs = driver.find_elements(By.CLASS_NAME, "most-wanted-customfields")

    div_one_labels = about_divs[0].find_elements(By.CLASS_NAME, "field-label")
    div_one_data = about_divs[0].find_elements(By.CLASS_NAME, "field-value")
    for i in range(min(len(div_one_labels), len(div_one_data))):
        about[div_one_labels[i].text[:-2]] = div_one_data[i].text

    div_two_labels = about_divs[0].find_elements(By.CLASS_NAME, "field-label")
    div_two_data = about_divs[1].find_elements(By.CLASS_NAME, "field-value")
    for i in range(min(len(div_two_labels), len(div_two_data))):
        about[div_two_labels[i].text[:-2]] = div_two_data[i].text

    criminal_data["about"] = about

    # get extra info (if it exists)
    div_three_data = about_divs[2].find_elements(By.CLASS_NAME, "field-value")
    if len(div_three_data) > 0:
        criminal_data["Extra Info"] = div_three_data[0].text

    # navigate back to most wanted page
    # driver.get("https://www.nationalcrimeagency.gov.uk/most-wanted-search")
    # click_pagination_button()

    return criminal_data



def main():
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
    click_pagination_button()
    
    # get list of all divs containing criminals
    criminal_divs = driver.find_elements(
        By.CLASS_NAME,
        "span4"
    )

    # get links to each criminal's page
    criminal_links = []
    for div in criminal_divs:
        link_element = div.find_element(By.TAG_NAME, "a")
        l = link_element.get_attribute('href')
        criminal_links.append(l)

    # initialize data
    return_json = {
        "source_code": "UK_MWL",
        "source_name": " UK Most Wanted List",
        "source_url": "https://www.nationalcrimeagency.gov.uk/most-wanted-search",
        "persons": []
    }
    persons = []
    
    # scrape and record data from each criminals page
    for l in criminal_links:
        criminal_data = scrape_criminal_data(l)
        # print(criminal_data)
        persons.append(criminal_data)

    return_json["persons"] = persons

    # turn dict into actual json
    return_json = json.dumps(return_json, indent=4)

    # write to json file
    with open("output.json", "w") as output:
        output.write(return_json)

    # close driver
    driver.close()




if __name__ == "__main__":
    main()