"""
Ordinary Scraping Using BS4 and Requests
Website: https://alpindustria.ru/ (russian shop for outdoor activities)

Protection: None
HTML: Can be easily obtained requesting URL
Pagination: Embedded in URL
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import fake_useragent

# Function For HTML Getting (Fake User-Agent Included) (1st Step)
def get_html(url):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    response = requests.get(url, headers = header)
    return BeautifulSoup(response.text, 'lxml')

# Function For HTML Parsing (2d Step)
def parse_html(html, items_storage):
    # Use CSS Selectors to find all itesm 
    items = html.select('div.prod.ddl_product')
    # Check whether items exist or not 
    if len(items) != 0:
        for item in items:
            # Collect the data into a dictionary (the best data structure, laster will be passed to Pandas)
            current_item = {
            'item': item.find('a', class_ = '_model ddl_product_link').text,
            'price': item.find('span', class_ = 'price_rub').text
        }
            items_storage.append(current_item)
    else:
        raise ValueError

# Final Output Foramt (3d Step)
def to_df(all_parsed_data):
    return pd.DataFrame(all_parsed_data)

# Main Part 
start_page = 0
res_data = []

# While the next page exist, continue parsing
while True:
    try:
        print(f'Current Page: {start_page}')
        html = get_html(f'https://perm.alpindustria.ru/?price_min=0&price_max=0&nal%5B%5D=-1&nal%5B%5D=94&div=catalog&num_on_page=20&page={start_page}&cat=odejda&subcat=kurtki&orderby=')
        parse_html(html, res_data)
        print(f'Total Size: {len(res_data)}')
        start_page += 1
    except:
        break

# Final Dataframe Making 
df = to_df(res_data)
print(df)