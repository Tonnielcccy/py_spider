# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SgeItem(scrapy.Item):
    date = scrapy.Field()
    hy = scrapy.Field()
    kpj = scrapy.Field()
    zgj = scrapy.Field()
    zdj = scrapy.Field()
    spj = scrapy.Field()
    zd = scrapy.Field()
    jqpjj = scrapy.Field()
    cjl = scrapy.Field()
    cjje = scrapy.Field()
    url = scrapy.Field()
