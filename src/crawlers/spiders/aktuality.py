import json
from pathlib import Path
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from langdetect import detect

ROOT_DIR = Path(__file__).resolve().parents[3]


class AktualitySpider(CrawlSpider):
    name = 'AktualitySpider'
    allowed_domains = ['referaty.aktuality.sk']
    start_urls = ['https://referaty.aktuality.sk']

    output_file = open(ROOT_DIR.joinpath('data/aktuality.json'), 'a+', encoding='utf8')

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=False,
                unique=True
            ),
            follow=True,
            callback='parse_items'
        )
    ]

    def parse_items(self, response):
        current_item = {}

        text = response.xpath("//*[@id=\"vpravo\"]/div/div/div[1]/div[@class=\"obsah\"]//text()").extract()
        if len(text) == 0:
            return

        title = response.xpath("//*[@id=\"vpravo\"]//h1[@itemprop=\"headline\"]//text()").extract()
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
