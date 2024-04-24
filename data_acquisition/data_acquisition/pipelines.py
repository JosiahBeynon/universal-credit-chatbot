# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os
import csv
from scrapy import signals
from scrapy.exceptions import DropItem


# from test_spider import TestSpider

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DataAcquisitionPipeline:
    def process_item(self, item, spider):
        return item
    

url_exceptions = [
    'calls-for-evidence',
    'case-studies',
    'collections',
    'consultations',
    'drug',
    'hmrc-internal-manuals',
    'landspreading',
    'news',
    'piper',
    'pippa',
    'publications',
    'research',
    'speeches',
    'statistics',
    'tribunal'
]

class UrlFilterPipeline:
    def __init__(self):
        self.exceptions = re.compile('|'.join(url_exceptions))
        self.filename = 'chosen_urls.csv'
        self.file = None
        self.writer = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # Check if file exists and ask user for action
        if os.path.exists(self.filename):
            response = input(f"File {self.filename} already exists. Overwrite it? (y/n): ")
            if response.lower() != 'y':
                raise SystemExit("Operation cancelled by the user.")
        self.file = open(self.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Title', 'URL'])  # Write CSV header

    def process_item(self, item, spider):
        if self.exceptions.search(item['url']):
            raise DropItem(f"URL filtered out: {item['url']}")
        else:
            self.writer.writerow([item['title'], item['url']])
            return item

    def spider_closed(self, spider):
        if self.file:
            self.file.close()
            self.file = None
