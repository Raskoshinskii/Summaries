# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# With items we can store scraping data into some fields and make data cleaning

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

'''
MapCompose:
Allows taking a set of functions that can be later applied
in an order in which they are provided (i.e. own pipelines can be defined for data processing)

TakeFirst:
Takes first not null value

'''

# Custom functions can be defined as well
'''
For example a function for removing sth
def remove_value(str, symbol):
    return str.replace('symbol', '').strip()

All defined functions can be then passed to the MapCompose for data processing
'''

class AlpindustriaScraperItem(scrapy.Item):
    # Can Define Fileds For Scraping Data and Process Them
    # We remove HTML tags from a field and then take the first not null falue after tags removing 
    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    link = scrapy.Field()

