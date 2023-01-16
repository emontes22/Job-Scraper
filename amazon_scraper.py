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
	print(soup)
	print(URL)
	break