from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json

def searchCanadianTire(product):
    # init and open webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # ignore certificates
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.canadiantire.ca/en.html')
    # Search for product
    searchBox = driver.find_element_by_id('global-atlas-search__input').send_keys(product)
    searchSubmit = driver.find_element_by_id('global-search__submit').click()


searchCanadianTire('bike')