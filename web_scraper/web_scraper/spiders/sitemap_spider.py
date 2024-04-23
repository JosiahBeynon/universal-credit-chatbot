from scrapy.spiders import SitemapSpider

class GovUKSpider(SitemapSpider):
    name = 'govuk_benefits'
    allowed_domains = ['www.gov.uk']
    sitemap_urls = ['https://www.gov.uk/sitemap.xml']

    # Sitemap filters can be regex expressions that cover your topics of interest
    sitemap_rules = [
        (r'/universal-credit', 'parse_benefits'),
        (r'/tax-credits', 'parse_benefits'),
        (r'/childcare', 'parse_benefits'),
        (r'/self-employment', 'parse_benefits'),
        (r'/benefits', 'parse_benefits')
    ]

    def parse_benefits(self, response):
        """
        Extract and process information from the benefit-related pages
        """
        title = response.xpath('//title/text()').get()
        url = response.url
        # You can extract more data here as per your requirement
        return {
            'title': title,
            'url': url
        }

# This spider will automatically follow the sitemap(s) and apply the specified filters
