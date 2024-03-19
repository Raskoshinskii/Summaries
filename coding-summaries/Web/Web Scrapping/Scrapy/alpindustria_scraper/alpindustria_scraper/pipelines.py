# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



'''
1. Make Sure that pipeline is activated:
    - Go to setting.py
    - Uncomment ITEM_PIPELINES 

2. Define connection and collection properties
3. Define data inserting in process_item function
'''

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class AlpindustriaScraperPipeline:

    def __init__(self):
        # Define a property for connection
        self.connection = pymongo.MongoClient(
            'localhost',
            27017
        )
        # Define DB creation
        db = self.connection['aplindustria']
        # Define Collection Creation
        self.collection = db['aplindustria']


    def process_item(self, item, spider):
        # Define Data Inserting
        self.collection.insert(dict(item))
        return item
