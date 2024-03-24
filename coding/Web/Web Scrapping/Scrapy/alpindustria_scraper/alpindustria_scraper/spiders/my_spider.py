import scrapy
from alpindustria_scraper.items import AlpindustriaScraperItem # Have to Import the Item Class
from scrapy.loader import ItemLoader

# Step 1 Create Your Own Spider Class (Must be inherited from scrapy.Spider)
class AlpIndustriaSpider(scrapy.Spider):
    name = 'AlpIndustria' # Every spider must have a name 
    start_urls = ['https://perm.alpindustria.ru/?price_min=0&price_max=0&nal%5B%5D=-1&nal%5B%5D=94&div=catalog&num_on_page=20&page=0&cat=odejda&subcat=kurtki&orderby=']
    base_url = 'https://perm.alpindustria.ru'

    #  Define the main function parse
    def parse(self, response):
        for item in response.css('div.prod.ddl_product'):
            # Data extraction and processing using ItemLoader
            loader = ItemLoader(item = AlpindustriaScraperItem(), selector = item)
            # Use CSS selectors to find the data (found data then processed using AlpindustriaScraperItem Class)
            loader.add_css('name', 'a._model.ddl_product_link') 
            loader.add_css('price', 'span.price_rub')
            loader.add_css('link', 'a._model.ddl_product_link::attr(href)')
            
            yield loader.load_item()

        # To emplement pagination we have to find next page button 
        next_page_link = response.css('a.next').attrib['href']
        # The last page doesn't have the next page button
        if next_page_link is not None:
            next_page = self.base_url + response.css('a.next').attrib['href']
            yield response.follow(next_page, callback = self.parse)
        

'''
# This is Example without items 

for item in response.css('div.prod.ddl_product'):
    link = self.base_url + item.css('a._model.ddl_product_link').attrib['href']
    yield {
            'name': item.css('a._model.ddl_product_link::text').get(),
            'price': item.css('span.price_rub::text').get(),
            'link': link
    }

# Another Example

item = AlpindustriaScraperItem()
for item in response.css('div.prod.ddl_product'):
    link = self.base_url + item.css('a._model.ddl_product_link').attrib['href']

    item['name'] = item.css('a._model.ddl_product_link::text').get()
    item['price'] = item.css('span.price_rub::text').get()
    item['link'] = link

    yield item

'''