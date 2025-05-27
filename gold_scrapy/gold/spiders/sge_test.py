import scrapy
import re
import csv
from datetime import datetime
from scrapy.http import Request
from tqdm import tqdm

class SgeSpider(scrapy.Spider):
    name = "sge_test"
    allowed_domains = ["www.sge.com.cn"]
    start_urls = ["https://www.sge.com.cn/sjzx/mrhqsj"]

    def __init__(self, max_pages=None, max_retries=3, **kwargs):
        super().__init__(**kwargs)
        self.max_pages = int(max_pages) if max_pages else None
        self.max_retries = int(max_retries)
        self.all_data = []
        self.failed_urls = []
        # 初始化进度条
        self.total_pages = self.max_pages or 385  # 如果未指定 max_pages，假设一个默认值
        self.page_progress = tqdm(total=self.total_pages, desc="Pages Crawled", unit="page")
        self.item_count = 0
        self.item_progress = tqdm(desc="Items Scraped", unit="item")

    def parse(self, response):
        for item in response.css('li.lh45.border_ea_b'):
            links = item.css('a.title::attr(href)').getall()
            for link in links:
                yield response.follow(link, callback=self.parse_detail, meta={'page': 1, 'retries': 0})

        # 自动翻页并更新进度
        next_page_div = response.css("div.btn.border_ea.noLeft_border[onclick*='gotoPage']")
        if next_page_div:
            onclick = next_page_div.attrib.get('onclick')
            if onclick:
                match = re.search(r"gotoPage\('/sjzx/mrhqsj\?p=','(\d+)'\)", onclick)
                if match:
                    current_page = int(match.group(1))
                    self.page_progress.update(1)  # 更新页面进度
                    if self.max_pages is not None and current_page >= self.max_pages:
                        self.logger.info(f"达到最大页码 {self.max_pages}，停止爬取。")
                        self.page_progress.close()
                        return
                    next_page = f"https://www.sge.com.cn/sjzx/mrhqsj?p={current_page}"
                    yield response.follow(next_page, callback=self.parse, meta={'page': current_page})

    def parse_detail(self, response):
        date = response.css("div.title p span::text").get()
        retries = response.meta.get('retries', 0)
        rows = response.css('table tr')
        data = []

        for row in rows:
            hy = (row.css('td:nth-child(1)::text').get() or '')
            kpj = (row.css('td:nth-child(2)::text').get() or '')
            zgj = (row.css('td:nth-child(3)::text').get() or '')
            zdj = (row.css('td:nth-child(4)::text').get() or '')
            spj = (row.css('td:nth-child(5)::text').get() or '')
            zd = (row.css('td:nth-child(6)::text').get() or '')
            jqpjj = (row.css('td:nth-child(7)::text').get() or '')
            cjl = (row.css('td:nth-child(8)::text').get() or '')
            cjje = (row.css('td:nth-child(9)::text').get() or '')
            if hy:
                data.append(
                    {
                        'date': date,
                        'hy': hy.strip(),
                        'kpj': kpj.strip(),
                        'zgj': zgj.strip(),
                        'zdj': zdj.strip(),
                        'spj': spj.strip(),
                        'zd': zd.strip(),
                        'jqpjj': jqpjj.strip(),
                        'cjl': cjl.strip(),
                        'cjje': cjje.strip(),
                        'url': response.url
                    }
                )

        if data:
            self.all_data.extend(data)
            self.item_count += len(data)
            self.item_progress.update(len(data))
            self.logger.info(f"解析完成：{response.url}，抓取 {len(data)} 条记录")
        else:
            if retries < self.max_retries:
                self.logger.error(f"解析失败：{response.url}，抓取 0 条记录，重试次数 {retries + 1}/{self.max_retries}")
                yield Request(
                    response.url,
                    callback=self.parse_detail,
                    meta={'page': 1, 'retries': retries + 1},
                    dont_filter=True
                )
            else:
                self.logger.error(f"解析失败：{response.url}，达到最大重试次数 {self.max_retries}，放弃")

        yield {'data': data}

    def closed(self, reason):
        # 关闭进度条
        self.page_progress.close()
        self.item_progress.close()

        # 保存数据到CSV
        try:
            filename = f'data_{datetime.now().strftime("%Y%m%d")}.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'date', 'hy', 'kpj', 'zgj', 'zdj', 'spj', 'zd', 'jqpjj', 'cjl', 'cjje', 'url'
                ])
                writer.writeheader()
                writer.writerows(self.all_data)
            self.logger.info(f"爬取完成，数据已保存到 {filename}，共抓取 {self.item_count} 条记录")
        except Exception as e:
            self.logger.error(f"保存 CSV 失败：{e}")
