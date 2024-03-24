import requests
from bs4 import BeautifulSoup
import fake_useragent
import pandas as pd

def get_html(url):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    response = requests.get(url, headers = header)
    return BeautifulSoup(response.text, 'lxml')

all_items = []

page = 1
while True:
    try:
        print(f'Parsing Page: {page}')
        home_page = f'https://www.citilink.ru/catalog/computers_and_notebooks/parts/videocards/?p={page}'
        html = get_html(home_page)
        items = html.select('div.product_data__gtm-js.product_data__pageevents-js.ProductCardVertical.js--ProductCardInListing.ProductCardVertical_normal.ProductCardVertical_shadow-hover.ProductCardVertical_separated')
        if len(items) != 0:
            for item in items:
                name = item.get('data-params').split(',')[4].lstrip('"shortName":"')
                price = int(item.get('data-params').split(',')[2].lstrip('"price":'))
                try:
                    stars = item.find('span', class_ = 'ProductCardVerticalMeta__count IconWithCount__count js--IconWithCount__count').text.strip('\n ')
                except:
                    stars = 'None'
                try:
                    reviews = item.find_all('span', class_ = 'ProductCardVerticalMeta__count IconWithCount__count js--IconWithCount__count')[1].text.strip('\n ')
                except:
                    reviews = 'None'  
                current_item = {
                    'name': name,
                    'price': price,
                    'stars:': stars,
                    'reviews': reviews
                }
                all_items.append(current_item)
            print('Parsed Successfully')
            page += 1
        else:
            raise ValueError
    except:
        break

df = pd.DataFrame(all_items)
print(df.head(15))