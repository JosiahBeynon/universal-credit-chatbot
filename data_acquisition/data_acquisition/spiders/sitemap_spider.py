import re
from scrapy.spiders import SitemapSpider
from scrapy import Item, Field

class URLItem(Item):
    url = Field()

class GovUKSpider(SitemapSpider):
    name = 'govuk_benefits'
    allowed_domains = ['www.gov.uk']
    sitemap_urls = ['https://www.gov.uk/sitemap.xml']

    # Compile inclusion patterns for URL filtering
    inclusion_patterns = re.compile('|'.join([
        '.*allowance.*',
        '.*benefit.*',
        '.*childcare.*',
        '.*self-employment.*',
        '.*tax-credit.*',
        '.*universal-credit.*',
        '.*/pip.*',
    ]))

    # Compile exclusion patterns for URL filtering
    url_exceptions = re.compile('|'.join([
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
    ]))


    def sitemap_filter(self, entries):
        for entry in entries:
            url = entry['loc']
            # Include URLs based on specific patterns and exclude based on exceptions
            if self.inclusion_patterns.search(url) and not self.url_exceptions.search(url):
                print(url)
                yield URLItem(url=url)
