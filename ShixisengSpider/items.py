# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ShixisengJobspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位
    collection = 'Job'

    uuid = Field()
    iname = Field()
    month = Field()
    maxsal = Field()
    minsal = Field()
    city = Field()
    scale = Field()
    reslan = Field()
    attraction = Field()
    ftype = Field()
    collected = Field()
    cuuid = Field()
    degree = Field()
    address = Field()
    chance = Field()
    endtime = Field()
    day = Field()
    info = Field()
    url = Field()
    industry = Field()
    refresh = Field()
    cname = Field()



class ShixisengCospiderItem(scrapy.Item):
    # 公司
    collection = 'Co'

    cuuid = Field()
    logo = Field()
    scale = Field()
    start_time = Field()
    description = Field()
    tags = Field()
    reg_num = Field()
    com_url = Field()
    address = Field()
    reg_capi = Field()
    info = Field()
    name = Field()
    pranum = Field()
    url = Field()
    industry = Field()
    cname = Field()
    com_type = Field()