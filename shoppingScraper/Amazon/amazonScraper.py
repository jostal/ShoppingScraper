from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json


def searchAmazon(product):
    # init and open web driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.amazon.ca')
    #Search for product
    searchBox = driver.find_element_by_id('twotabsearchtextbox').send_keys(product)
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
        clickNext = driver.find_element_by_xpath('//*[@class="a-pagination"]/li[7]').click()
        print("Page " + str(pageCur) + " grabbed")
    driver.quit()

    # Write collected url links to searchResultsURLs.txt
    with open('searchResultsURLs.txt', 'w') as filehandle:
        for pageURL in urls:
            filehandle.write('%s\n' % pageURL)

    print("PAGE LINKS ADDED")


#scrapehero code
def scrape(url):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)

searchAmazon('bikes')

e = Extractor.from_yaml_file('searchResults.yaml')

# product_data = []
with open("searchResultsURLs.txt",'r') as urllist, open('searchResultsOutput.json','w') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url)
        if data:
            for product in data['products']:
                product['search_url'] = url
                print("Saving Product: %s"%product['title'].encode('utf8'))
                json.dump(product, outfile)
                outfile.write("\n")
                # sleep(5)