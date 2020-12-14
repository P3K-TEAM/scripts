import json
from pathlib import Path
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from langdetect import detect

ROOT_DIR = Path(__file__).resolve().parents[3]


class ReferatySpider(CrawlSpider):
    name = 'ReferatySpider'
    allowed_domains = ['referaty.centrum.sk']
    start_urls = ['https://referaty.centrum.sk']

    output_file = open(ROOT_DIR.joinpath('data/referaty.json'), 'a+', encoding='utf8')

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=False,
                unique=True,
                deny=[r".*download\.php.*", r".*vote\.php.*"],
            ),
            follow=True,
            callback='parse_items'
        )
    ]

    def parse_items(self, response):
        current_item = {}

        if not response.url.endswith("?print=1"):
            return

        TITLE_SELECTOR = "h1::text"
        TEXT_SELECTOR = "td>div *::text"

        title = response.css(TITLE_SELECTOR).extract_first()
        text = response.css(TEXT_SELECTOR).extract()
        url = response.url.replace('?print=1', '')

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
