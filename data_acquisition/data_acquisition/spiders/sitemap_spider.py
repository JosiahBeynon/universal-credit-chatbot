import os
import re
import csv
from scrapy.spiders import SitemapSpider

class GovUKSpider(SitemapSpider):
    name = 'govuk_benefits'
    allowed_domains = ['www.gov.uk']
    # start_urls = [
    # 'https://www.gov.uk/pension-credit',
    # 'https://www.gov.uk/jobseekers-allowance',
    # 'https://www.gov.uk/hmrc-internal-manuals/tax-credits-manual/tcm0286140'
    # ]   
    custom_settings = {
        # 'DOWNLOAD_DELAY': 0.05,  # Delay in seconds between requests to the same website
        'ITEM_PIPELINES': {
            'data_acquisition.pipelines.UrlFilterPipeline': 300,
        }
    }
    
    sitemap_urls = ['https://www.gov.uk/sitemap.xml']

    sitemap_rules = [
        ('.*universal-credit.*', 'parse_urls'),
        ('.*tax-credit.*', 'parse_urls'),
        ('.*childcare.*', 'parse_urls'),
        ('.*self-employment.*', 'parse_urls'),
        ('.*benefit.*', 'parse_urls'),
        # ('.*disability-living-allowance.*', 'parse_urls'),
        ('.*allowance.*', 'parse_urls'),
        ('.*/pip.*', 'parse_urls'),
        ('.*allowance.*', 'parse_urls')
    ]

    def parse_urls(self, response):
        title = response.xpath('//title/text()').get()
        url = response.url
        return {
            'title': title,
            'url': url
        }

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    process.crawl(GovUKSpider)
    process.start()
