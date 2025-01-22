# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class TestprojectPipeline:
    def process_item(self, item, spider):
        if (item['title'] and item['image'] and item['description']):
            item['title'] = clean_spaces(item['title'])
            return item
        else:
            raise DropItem("Missing a component")


class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # Connexion à MongoDB lors de l'ouverture du spider
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # Fermeture de la connexion à MongoDB après l'exécution du spider
        self.client.close()

    def process_item(self, item, spider):
        # Insertion de l'item dans une collection MongoDB
        self.db["articles"].insert_one(dict(item))  # spider.name = nom de la collection
        return item


def clean_spaces(string):
        if string:
            return " ".join(string.split())
