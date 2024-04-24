from scrapy import signals
import csv

class UrlFilterPipeline:
    def __init__(self):
        self.filename = 'filtered_urls.csv'
        self.file = None
        self.writer = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open(self.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['URL'])  # Write CSV header

    def process_item(self, item, spider):
        self.writer.writerow([item['url']])
        return item

    def spider_closed(self, spider):
        self.file.close()
