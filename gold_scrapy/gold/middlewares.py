# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GoldSpiderMiddleware:
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


class GoldDownloaderMiddleware:
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
        # 限制为桌面端浏览器
        self.ua = UserAgent(browsers=['edge', 'chrome'], os=['windows'])

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        # 设置随机 User-Agent
        request.headers['User-Agent'] = self.ua.random
        logging.debug(f"User-Agent: {request.headers.get('User-Agent')}")
        return None


class CustomHeadersMiddleware:
    def __init__(self):
        # SGE 网站的 headers，基于提供的示例
        self.default_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'connection': 'keep-alive',
            'host': 'www.sge.com.cn',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1'
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        # 设置默认 headers
        for key, value in self.default_headers.items():
            request.headers.setdefault(key, value)
        # 动态设置 Referer（仅在分页请求时）
        if 'page' in request.meta:
            request.headers['Referer'] = f'https://www.sge.com.cn/sjzx/mrhqsj?p={request.meta["page"]}'
        logging.debug(f"Headers: {request.headers}")
        return None


class CustomCookiesMiddleware:
    def __init__(self):
        # SGE 网站的 cookies，基于提供的示例
        self.default_cookies = {
            'Hm_lvt_9165e30c92968eb1baa5e3eb5f34dc60': '1747722888,1747916156',
            'HMACCOUNT': '3B724E87B13FCDC9',
            'JSESSIONID': '82A5F12A7382810A41CAF5C8037D2781',
            'Hm_lpvt_9165e30c92968eb1baa5e3eb5f34dc60': '1747925647'
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        # 设置默认 cookies
        request.cookies = self.default_cookies
        logging.debug(f"Cookies: {request.cookies}")
        return None
