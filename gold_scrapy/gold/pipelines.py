from scrapy.exceptions import DropItem
import csv


class CsvPipeline:
    def open_spider(self, spider):
        self.file = open(spider.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=spider.csv_fields)
        self.writer.writeheader()

    def process_item(self, item, spider):
        # 直接写入，不做类型转换
        self.writer.writerow({field: item.get(field, '') for field in spider.csv_fields})
        return item

    def close_spider(self, spider):
        self.file.close()