import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# To allow automated access to Amazondata
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

search_item = 'raspberry pi'.replace(' ', '+')
URL = 'https://www.amazon.com/s?k={0}'.format(search_item)

items = []

for i in range(1, 11):
    print('Searching {0}...'.format(URL + '&page={0}'.format(i)))
    response = requests.get(URL + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all(
        'div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    # Find the name of all products
    for result in results:
        product_name = result.h2.text.strip()

        # For each product found, get the rating stars and count
        try:
            product_rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all(
                'span', {'aria-label': True})[1].text.strip()

        # If not found then continue to run the next block of code
        except AttributeError:
            continue

        # For each product found, get the price and url
        try:
            whole_price = result.find('span', {'class': 'a-price-whole'}).text
            fraction_price = result.find(
                'span', {'class': 'a-price-fraction'}).text
            total_price = float(whole_price + fraction_price)
            product_url = 'https://www.amazon.com' + result.h2.a['href']
            items.append([product_name, product_rating,
                         rating_count, total_price, product_url])

        # If not found then continue to run the next block of code
        except AttributeError:
            continue

    # Time to sleep before the next page gets scanned
    sleep(1.5)

# Pandas to format the items and save it to a csv file
df = pd.DataFrame(items, columns=[
                  'Product', 'Rating Stars', 'Rating Count', 'Price', 'Product Link'])
df.to_csv('{0}.csv'.format(search_item), index=False)
