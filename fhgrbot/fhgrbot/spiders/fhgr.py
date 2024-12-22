
from scrapy.spiders import SitemapSpider
from ..items import FhgrbotItem

class FhgrSpider(SitemapSpider):
    name = "fhgr"
    sitemap_urls = ["https://www.fhgr.ch/sitemap.xml"]

    def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            if link.endswith('.pdf'):
                parts = link.split('/')
                second_last_part = parts[-2]
                filename_parts = [second_last_part, '#', parts[-1]]
                print(link)
                yield FhgrbotItem(
                    file_urls=['https://www.fhgr.ch' + link],
                    filename=''.join(filename_parts)
                )