# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from .items import ShixisengJobspiderItem, ShixisengCospiderItem

class MongoPipeline(object):
    def __init__(self, local_mongo_host, local_mongo_port, mongo_db):
        self.local_mongo_host = local_mongo_host
        self.local_mongo_port = local_mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):

        return cls(
            local_mongo_host=crawler.settings.get('LOCAL_MONGO_HOST'),
            local_mongo_port=crawler.settings.get('LOCAL_MONGO_PORT'),
            mongo_db=crawler.settings.get('DB_NAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.local_mongo_host, self.local_mongo_port)
        # 数据库名
        self.db = self.client[self.mongo_db]
        # 以Item中collection命名 的集合  添加index
        self.db[ShixisengJobspiderItem.collection].create_index([('uuid', pymongo.ASCENDING)])
        self.db[ShixisengCospiderItem.collection].create_index([('cuuid', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ShixisengJobspiderItem):
            self.db[item.collection].update({'uuid': item.get('uuid')},
                                            {'$set': item},
                                            True
                                            )

        elif isinstance(item, ShixisengCospiderItem):
            self.db[item.collection].update({'cuuid': item.get('cuuid')},
                                            {'$set': item},
                                            True
                                            )

        return item



import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline

class ShixisengImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, ShixisengCospiderItem):
            url = item['logo']
            yield scrapy.Request(url, meta={'item': item})


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_name1 = item['name']
        image_name1 = re.sub(r'[？\\*|“<>:/]', '', str(image_name1))
        image_name2 = request.url.split('/')[-1]
        # path = u'{}/{}'.format(item['title'], image_name)
        path = image_name1 + image_name2
        return path