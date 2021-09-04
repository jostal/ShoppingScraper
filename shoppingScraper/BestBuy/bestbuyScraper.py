from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json

# formats product string to required format by bestbuy
def formatProduct(product):
    return product.replace(" ", '+')

# Searches BestBuy for product
def searchBestBuy(product):
    product = formatProduct(product)
    # init and open web driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.bestbuy.ca/en-ca/search?search=' + product)
    # Search for product
    driver.implicitly_wait(7)

    driver.quit()



def scrapeBestBuy(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.bestbuy.ca/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        print("Page %s must have been blocked by BestBuy as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)

product = 'video card'
url = 'https://www.bestbuy.ca/en-ca/search?search=' + product
searchBestBuy(product)

e = Extractor.from_yaml_file('searchResults.yaml')

with open('searchResultsOutput.json', 'w') as outfile:
    data = scrapeBestBuy('https://www.bestbuy.ca/en-ca/search?search=' + product)
    if data:
        print(data['products'])
        for product in data['products']:
            print("Saving Product: %s"%product['title'].encode('utf8'))
            json.dump(product, outfile)
            outfile.write("\n")


    


