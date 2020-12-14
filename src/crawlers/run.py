import scrapy
import sys
from scrapy.crawler import CrawlerProcess
from spiders.aktuality import AktualitySpider
from spiders.referaty import ReferatySpider
from spiders.zones import ZonesSpider

crawlers = {
    'referaty': ReferatySpider,
    'aktuality': AktualitySpider,
    'zones': ZonesSpider
}

# load user's choice of spider
crawler_choice = sys.argv[1]

process = CrawlerProcess()
process.crawl(crawlers[crawler_choice])
process.start()
