

from ssl import Options
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


import codecs

import re

import urllib

import pandas as pd


options = Options()
options.add_argument(" - headless")
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))

url = "https://www.amazon.in/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2"
driver.get(url)




def login_to_amazon(driver, username, password):

       
    driver.get("https://www.amazon.com/ap/signin")

    # Find the username and password fields
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located_by_xpath("//input[@id='ap_email']"))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located_by_xpath("//input[@id='ap_password']"))

    # Enter the username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Find and click the login button
    signin_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable_by_xpath("//input[@id='signInSubmit']"))
    signin_button.click()

    # Wait for successful login (adjust the wait time as needed)
    wait=WebDriverWait(driver, 20)

    wait.untill(EC.presence_of_element_located_by_xpath("//input[@id='nav-link-accountList']"))


def scrape_best_sellers(driver, category_url):
    driver.get(category_url)

    # Scroll down to load more products
    while True:
        driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        time.sleep(20)
        try:
            load_more_button = driver.find_element_by_xpath("//input[@data-action='show-more']")
            load_more_button.click()
        except:
            break

    products_data = driver.find_elements_by_xpath("//input[@data-component-type='s-search-result']")
    soup = BeautifulSoup(products_data.get_attribute('innerHTML'), 'html.parser')

    product_data = []
    for product in products_data:
        try:
            product_name = products_data.find_element_by_xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']").text
            product_price = products_data.find_element_by_xpath(".//span[@class='a-price-whole']").text
            sale_discount = products_data.find_element_by_xpath(".//span[@class='a-price-off']").text
            best_seller_rating = products_data.find_element_by_xpath(".//span[@class='a-icon-alt']").text
            ship_from = products_data.find_element_by_xpath(".//span[@class='a-color-secondary a-size-base a-text-bold']").text
            sold_by = products_data.find_element_by_xpath(".//span[@class='a-size-base a-color-secondary a-text-bold']").text
            rating = products_data.find_element_by_xpath(".//span[@class='a-icon-alt']").text
            product_description = products_data.find_element_by_xpath(".//span[@class='a-size-base a-color-base a-text-normal']").text
            # ... other details like number bought, images, etc. can be extracted using similar XPath expressions

            number_bought_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located_by.CSS_SELECTOR(".//span[@class='number-bought-selector']"))

            number_bought = number_bought_element.text

            category_name = products_data.find_element_by_xpath(".//span[@class='a-icon-alt']").text

            url = 'https://www.amazon.in/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            for img in soup.find_all('img'):
                src = img.get('src')
                urllib.request.urlretrieve(src, 'image_' + src.split('/')[-1])

            def scrape_category(url):
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

    

            products_data = []
            for link in products_data:
                product_url = link['href']
                product_response = requests.get(product_url)
                product_soup = BeautifulSoup(product_response.content, 'html.parser')

                product_name = product_soup.find('h1', {'id': 'productTitle'}).text.strip()
                product_price = product_soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()
                sale_discount = product_soup.find('span', {'id': 'priceoff'}).text.strip()
                best_seller_rating = product_soup.find('span', {'id': 'bestRating'}).text.strip()
                ship_from = product_soup.find('span', {'id': 'shipsFrom'}).text.strip()
                sold_by = product_soup.find('span', {'id': 'soldby'}).text.strip()
                rating = product_soup.find('span', {'id': 'rating'}).text.strip()
                product_description= product_soup.find('span', {'id': 'product_discription'}).text.strip()
                number_bought = product_soup.find('span', {'id': 'number_brought_element'}).text.strip()
                category_name = product_soup.find('span', {'id': 'category_name'}).text.strip()
                img = product_soup.find('span', {'id': 'img'}).text.strip()

            # Filter for products with discounts greater than 50%
            if "50%" in sale_discount:
                products_data.append([product_name, product_price, sale_discount, best_seller_rating, ship_from, sold_by, rating, product_description,number_bought,category_name,img])
        except:
            pass

    return pd.DataFrame(products_data)
    

# Replace with your actual Amazon credentials
username = "paragshemankar@gmil.com"
password = "Parag2507@"

# List of 10 category URLs
def extract_category_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all category links (adjust the selector as needed)
    category_links = soup.find_all('a', {'class': 'category-link'})  # Replace with the actual class or ID

    # Extract the URLs from the links
    urls = [link['href'] for link in category_links[:10]]  # Get the first 10 URLs

    return urls

# Example usage:
base_url = "https://www.amazon.in/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2"  # Replace with the base URL of the website
category_page_url = f"{"https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0"}/categories"  # Replace with the actual category page URL

category_urls = extract_category_urls(category_page_url)


def login_to_amazon(driver, username, password):
    driver.get("https://www.amazon.com/ap/signin")

    # Find the username and password fields
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located_by_xpath("//input[@id='ap_email']"))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located_by_xpath("//input[@id='ap_password']"))

    # Enter the username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Find and click the login button
    signin_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable_by_xpath("//input[@id='signInSubmit']"))
    signin_button.click()

    


# Create a Pandas DataFrame
df = pd.DataFrame()
# Save the data to a CSV file
df.to_csv("amazon_best_sellers.csv", index=False)

driver.quit()