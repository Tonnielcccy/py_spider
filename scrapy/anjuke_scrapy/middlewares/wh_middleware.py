# _*_ coding: utf-8 _*_
# @Time: 2025/5/22 13:56
# @Email: aocelary@qq.com
# @Author: Tonnie_lcccy
# @File: wh_middleware.py


# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# anjuke_project/middlewares/wuhan_middleware.py

class WuhanMiddleware:
    def process_request(self, request, spider):
        print("[武汉中间件] 请求：", request.url)



class AnjukeScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AnjukeScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

from fake_useragent import UserAgent
import logging

class RandomUserAgentMiddleware:
    def __init__(self):
        self.ua = UserAgent(browsers=['edge', 'chrome'], os=['windows'])  # 限制为桌面端浏览器

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random
        logging.debug(f"User-Agent: {request.headers.get('User-Agent')}")
        return None

class CustomHeadersMiddleware:
    def __init__(self):
        self.default_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'wh.zu.anjuke.com',
            'Origin': 'https://wh.zu.anjuke.com',
            'Pragma': 'no-cache',
            'Referer': 'https://wh.zu.anjuke.com/fangyuan/',
            'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        for key, value in self.default_headers.items():
            request.headers.setdefault(key, value)
        # 动态更新 Referer
        if 'page' in request.meta:
            request.headers['Referer'] = f'https://wh.zu.anjuke.com/fangyuan/p{request.meta["page"]}/'
        logging.debug(f"Headers: {request.headers}")
        return None

class CustomCookiesMiddleware:
    def __init__(self):
        self.default_cookies = {
            'xxzlxxid': 'pfmxJOpkIE6CX84OdWhX6bK18SkE3r1Ht7Wy7hiJHnx3bokFovp05UjPon5c0nMvbj1l',
            'sessid': '12BF0D2F-FFF4-4F97-A5D4-E095E41D3015',
            'ctid': '22',  # 武汉城市 ID
            'aQQ_ajkguid': '64AFE55A-E4D4-5B98-6F20-F4D44A12A23D',
            'xxzlclientid': '65989c6f-7377-4809-a6de-1746346137304',
            'isp': 'true',
            '58tj_uuid': 'a03fee21-fa2d-48df-858c-b3bb81c73d0c',
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        request.cookies = self.default_cookies
        logging.debug(f"Cookies: {request.cookies}")
        return None