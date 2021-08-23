from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json
import time


def searchAmazon(product):
    # init and open web driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.amazon.ca')
    #Search for product
    searchBox = driver.find_element_by_id('twotabsearchtexbox').send_keys(product)
    searchSubmit = driver.find_element_by_id('nav-search-submit-button').click()
    driver.implicitly_wait(5)   # wait for page to load
    # Find total number of pages if multiple pages exist
    try:
        numPages = driver.find_element_by_xpath('//*[@class="a-pagination"]/li[6]')
    except NoSuchElementException:
        numPages = driver.find_element_by_class_name('a-last').click()
        driver.implicitly_wait(3)
    
    #Iterate through all existing result pages and grab links
    urls = []
    for i in range(int(numPages.text)):
        pageCur = i + 1
        urls.append(driver.current_url)
        driver.implicitly_wait(5)
        clickNext = driver.find_element_by_class_name('a-last').click()
        print("Page " + str(pageCur) + " grabbed")
    driver.quit()

    # Write collected url links to searchResultsURLs.txt
    with open('searchResultsURLs.txt', 'w') as filehandle:
        for pageURL in urls:
            filehandle.write('%s\n' % pageURL)

    print("PAGE LINKS ADDED")