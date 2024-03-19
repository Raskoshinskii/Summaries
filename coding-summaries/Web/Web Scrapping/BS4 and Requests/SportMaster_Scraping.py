"""
Ordinary Scraping Using BS4 and Requests
Website: https://www.sportmaster.ru/ (russian shop for outdoor activities)

Protection: None
HTML: Can be easily obtained requesting URL
Pagination: Embedded in URL

"""

import requests
from bs4 import BeautifulSoup
import fake_useragent
import pandas as pd

def get_html(url):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    response = requests.get(url, headers=header)
    return BeautifulSoup(response.text, 'lxml')


scraped_items = []
home_page = 'https://www.sportmaster.ru/catalog/muzhskaya_odezhda/kurtki/?page=1'
html = get_html(home_page)
start_page = 1
end_page = int(html.find_all('a', class_='ajax-facet-value updateFacet scrollToTopPlease')[4].text)

for page in range(start_page, end_page+1):
    print(f'Parsing Page: {page}')
    current_html = f'https://www.sportmaster.ru/catalog/muzhskaya_odezhda/kurtki/?page={page}'
    items = html.find_all('div', class_='sm-category__item')
    for item in items:
        name = item.find('img').get('alt')
        price = item.select_one('sm-amount').get('params').split(' ')[1]
        try:
            stars = item.find('span', class_='sm-category__item-rating-stars').get('title')
        except:
            stars = 'None'
        try:
            reviews = item.find('span', class_='sm-category__item-rating-label').text.split(' ')[0].strip('\r\n')
        except:
            reviews = 'None'

        current_item = {
            'name': name,
            'price': price,
            'stars': stars,
            'reviews': reviews
        }
        scraped_items.append(current_item)

print(f'Total Items: {len(scraped_items)}')

# Final DataFrame
df = pd.DataFrame(scraped_items)
print(df)



















