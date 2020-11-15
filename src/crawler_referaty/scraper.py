import scrapy
import json
import os.path

class ReferatySpider(scrapy.Spider):
    name = 'referaty'
    dirname = os.path.dirname(__file__)
    output_file = open(os.path.join(dirname,'../../data/referaty.json'), 'a+')
    
    url = 'https://referaty.centrum.sk'
    allowed_domains = ['referaty.centrum.sk']

    current_item = {}

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):
       
        PRINT_SELECTOR = '[id="revsysln"] a[target="_blank"]::attr(href)'
        print_url = response.css(PRINT_SELECTOR).extract_first()

        if(print_url):
            
            LANGUAGE_SELECTOR = '.infobox tr:nth-child(4) img::attr(title)'
            language = response.css(LANGUAGE_SELECTOR).extract_first()

            self.current_item['language'] = language
            self.current_item['url'] = response.request.url

            yield scrapy.Request(
                url=response.urljoin(print_url), 
                callback=self.parse_printpage
                )

        for href in response.css('a::attr(href)').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
        

    def parse_printpage(self, response):

        TITLE_SELECTOR = "h1::text"
        TEXT_SELECTOR = "td>div::text"

        title = response.css(TITLE_SELECTOR).extract_first()
        text = response.css(TEXT_SELECTOR).extract()
        text = ''.join(text)

        self.current_item['title'] = title
        self.current_item['text'] = text

        json.dump(
            self.current_item,
            self.output_file, 
            indent=""
        )
            
        self.output_file.write(",\n")


        