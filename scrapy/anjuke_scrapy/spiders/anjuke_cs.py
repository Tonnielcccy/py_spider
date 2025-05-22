# _*_ coding: utf-8 _*_
# @Time: 2025/5/22 13:44
# @Email: aocelary@qq.com
# @Author: Tonnie_lcccy
# @File: anjuke_cs.py
import scrapy
from pathlib import Path
import re


class AnjukeSpider(scrapy.Spider):
    name = "anjuke_cs"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'anjuke_scrapy.middlewares.cs_middleware.ChangshaMiddleware': 400,
            'anjuke_scrapy.middlewares.cs_middleware.RandomUserAgentMiddleware': 401,
            'anjuke_scrapy.middlewares.cs_middleware.CustomHeadersMiddleware': 402,
            'anjuke_scrapy.middlewares.cs_middleware.CustomCookiesMiddleware': 403,
        }
    }
    allowed_domains = ["anjuke.com"]  # 限制爬虫范围
    start_urls = ["https://cs.zu.anjuke.com/?from=HomePage_TopBar"] # 起始网址

    def __init__(self, max_pages=None, **kwargs):
        # 设置最大爬取页数，可以动态修改scrapy crawl quotes -a max_pages=3，默认值为None表示不限制页数
        super().__init__(**kwargs)
        if max_pages is None:
            self.max_pages = None  # 表示不限制页数
        else:
            self.max_pages = int(max_pages)
        # 断点续爬
        if Path("visited_urls.txt").exists():
            with open("visited_urls.txt") as f:
                self.visited_urls = set(f.read().splitlines())
        else:
            self.visited_urls = set()

    def parse(self, response):
        if response.url in self.visited_urls:  # 检查当前网址是否已经爬取过
            return
        self.visited_urls.add(response.url)
        with open("visited_urls.txt", "a") as f:
            f.write(response.url + "\n")

        for box in response.css("div.zu-itemmod"):
            raw_location = box.css("div.zu-info address.details-item.tag").xpath("string(.)").get()
            location = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', raw_location).strip()

            raw_style = box.css("div.zu-info p.details-item.tag").xpath("string(.)").get()
            style = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', raw_style).strip()

            yield {
                "title": box.css("div.zu-info h3 a b.strongbox::text").get(),
                "style": style,
                "location": location,
                "tags": box.css("div.zu-info p.bot-tag span.cls-common::text").getall(),
                "broker": box.css("div.zu-info span.jjr-info::text").get(default=''),
                "price": box.css("div.zu-side strong.price::text").get(default=''),
                "unit": box.css("div.zu-side span.unit::text").get(default='')
            }

        # 获取当前页码
        match = re.search(r"/p(\d+)/", response.url)
        if match:
            current_page = int(match.group(1))
        else:
            current_page = 1

        # 检查当前页码是否超过最大页码
        if self.max_pages is not None and current_page >= self.max_pages:
            self.logger.info(f"达到最大页码 {self.max_pages}，停止爬取。")
            return

        # 继续翻页
        next_page = response.css("a.aNxt::attr(href)").get()  # 安居客的“下一页”按钮
        if next_page and next_page not in self.visited_urls:
            yield response.follow(next_page, meta={'page': current_page + 1}, callback=self.parse)

        else:
            self.logger.info(f"没有下一页或已访问：{response.url}")