import json
from pathlib import Path
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from langdetect import detect

ROOT_DIR = Path(__file__).resolve().parents[3]


class ZonesSpider(CrawlSpider):
    name = 'ZonesSpider'
    allowed_domains = ['zones.sk']
    start_urls = ['https://www.zones.sk/studentske-prace/']
    output_file = open(ROOT_DIR.joinpath('data/zones.json'), 'a+', encoding='utf8')

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=False,
                unique=True,
                deny=[r".*vyznamslova.*"],
            ),
            follow=True,
            callback='parse_items'
        )
    ]

    def parse_items(self, response):
        current_item = {}

        text = response.xpath("//*[@id=\"studentska_praca\"]/div[1]//text()").extract()

        if len(text) == 0:
            return

        title = response.xpath("/html/body//div[@id = \"obsah_left\"]/h1/text()").extract()
        url = response.url

        title = ''.join(title)
        text = ''.join(text)
        language = detect(text)

        current_item['url'] = url
        current_item['language'] = language
        current_item['title'] = title
        current_item['text'] = text

        json.dump(
            current_item,
            self.output_file,
            ensure_ascii=False,
            indent=""
        )
        self.output_file.write(",\n")

        yield {
            "url": current_item['url'],
            "lang": language,
            "title": current_item['title'],
            "text": current_item['text']
        }
