import scrapy
import json
import os.path

class ReferatySpider(scrapy.Spider):
    name = 'referaty'
    dirname = os.path.dirname(__file__)
    output_file = open(os.path.join(dirname,'../../data/referaty.json'), 'a+', encoding='utf8' )
    
    url = 'https://referaty.centrum.sk'
    allowed_domains = ['referaty.centrum.sk']

    def __init__(self):
        self.output_file.write("[\n")

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def close_spider(self, spider):
        self.output_file.write("]\n")
        self.output_file.close()

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):
        current_item = {}
        PRINT_SELECTOR = '[id="revsysln"] a[target="_blank"]::attr(href)'
        print_url = response.css(PRINT_SELECTOR).extract_first()

        if(print_url):
            
            LANGUAGE_SELECTOR = '.infobox tr:nth-child(4) img::attr(title)'
            language = response.css(LANGUAGE_SELECTOR).extract_first()

            current_item['language'] = language
            current_item['url'] = response.request.url

            yield scrapy.Request(
                url=response.urljoin(print_url), 
                callback=self.parse_printpage,
                meta={'current_item': current_item}
                )

        for href in response.css('a::attr(href)').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
        

    def parse_printpage(self, response):
        current_item = response.meta.get('current_item')
        TITLE_SELECTOR = "h1::text"
        TEXT_SELECTOR = "td>div *::text"

        title = response.css(TITLE_SELECTOR).extract_first()
        text = response.css(TEXT_SELECTOR).extract()
        text = ''.join(text)

        current_item['title'] = title
        current_item['text'] = text

        json.dump(
            current_item,
            self.output_file, 
            ensure_ascii=False,
            indent=""
        )
            
        self.output_file.write(",\n")


        