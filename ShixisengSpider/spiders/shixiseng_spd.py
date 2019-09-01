# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from pyquery import PyQuery as pq
from ..items import ShixisengCospiderItem, ShixisengJobspiderItem

class ShixisengSpdSpider(scrapy.Spider):
    name = 'shixiseng_spd'
    # allowed_domains = ['shixiseng.com']

    c = '全国'
    kw = '数据分析'  # 职位 可修改

    url_job = 'https://www.shixiseng.com/app/interns/search?s=-0&c={c}&d=&x=&i=&z=&k={kw}&page={page}&m='
    url_job_info = 'https://www.shixiseng.com/app/intern/info?uuid={uuid}'
    url_co = 'https://www.shixiseng.com/app/company/info?uuid={cuuid}'
    def start_requests(self):
        page = 1
        yield Request(self.url_job.format(c=self.c, kw=self.kw, page=page), callback=self.parse, meta={'page': page})


    def parse(self, response):
        res = json.loads(response.text)
        if res.get('msg'):
            for data in res.get('msg'):
                uuid = data.get('uuid')
                yield Request(self.url_job_info.format(uuid=uuid), callback=self.parse_job, meta={'uuid': uuid})

            page = response.meta['page']
            page = page + 1
            yield Request(self.url_job.format(c=self.c, kw=self.kw, page=page), callback=self.parse, meta={'page': page})

    def parse_job(self, response):

        item = ShixisengJobspiderItem()
        res = json.loads(response.text)
        data = res.get('msg')
        item['uuid'] = response.meta['uuid']
        item['iname'] = data.get('iname')
        item['month'] = data.get('month')
        item['maxsal'] = data.get('maxsal')
        item['minsal'] = data.get('minsal')
        item['city'] = data.get('city')
        item['scale'] = data.get('scale')
        item['reslan'] = data.get('reslan')
        item['attraction'] = ''.join(data.get('attraction'))
        item['ftype'] = data.get('ftype')
        item['collected'] = data.get('collected')
        item['cuuid'] = data.get('cuuid')
        item['degree'] = data.get('degree')
        item['address'] = data.get('address')
        item['chance'] = data.get('chance')
        item['endtime'] = data.get('endtime')
        item['day'] = data.get('day')

        info = data.get('info')
        item['info'] = ''.join(pq(info).text().replace('\xa0', '').split('\n'))

        item['url'] = data.get('url')
        item['industry'] = data.get('industry')
        item['refresh'] = data.get('refresh')
        item['cname'] = data.get('cname')
        yield item

        yield Request(self.url_co.format(cuuid=item['cuuid']), callback=self.parse_c, meta={'cuuid': item['cuuid']})

    def parse_c(self, response):
        item = ShixisengCospiderItem()
        res = json.loads(response.text)
        data = res.get('msg')
        item['cuuid'] = response.meta['cuuid']
        item['logo'] = data.get('logo')
        item['scale'] = data.get('scale')
        item['start_time'] = data.get('start_time')
        item['description'] = data.get('description')

        tags = data.get('tags').encode('utf-8').decode('unicode_escape')
        tags = tags.replace(']','').replace('[','')
        item['tags'] = ''.join([x.strip() for x in tags])

        item['reg_num'] = data.get('reg_num')
        item['com_url'] = data.get('com_url')
        item['address'] = data.get('address')
        item['reg_capi'] = data.get('reg_capi')

        info = data.get('info')
        item['info'] = ''.join(pq(info).text().replace('\xa0', '').split('\n'))

        item['name'] = data.get('name')
        item['pranum'] = data.get('pranum')
        item['url'] = data.get('url')
        item['industry'] = data.get('industry')
        item['cname'] = data.get('cname')
        item['com_type'] = data.get('com_type')

        yield item