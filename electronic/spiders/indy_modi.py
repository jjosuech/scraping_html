import scrapy
import json
from datetime import datetime

class SpotahomeSpider(scrapy.Spider):
    name = "indy_modi"
    allowed_domains = ["www.indyperuvapes.pe"]

    def start_requests(self):
        with open('indy.json', 'r', encoding='utf-8') as file:
            products = json.load(file)
        
        for product in products:
            url = product['link']
            yield scrapy.Request(url=url, callback=self.parse, meta={'product': product})

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        product = response.meta['product']
        listing = response.xpath("//div[contains(@class, 'center_column')]").get()

        if listing:
            #title_xpath = ".//div[contains(@class, 'product-template__content')]/div[1]/div[2]/div[2]/div[1]/h1/text()"
            title_xpath1 = ".//h1[contains(@class, 'product-single__title')]/text()"
            title = response.xpath(title_xpath1).get()  # Use response directly

            old_price_css = ".//ul[contains(@class, 'list-prope')]/li[5]/a/text()"
            sale_price_css = ".//div[contains(@class, 'product-meta')]/div[contains(@class, 'content_price')]/span[contains(@class, 'sale-price')]/text()"
            sale_price_css2 = ".//div[contains(@class, 'product-meta')]/div[contains(@class, 'content_price')]/span[1]/text()"
            old_price = response.xpath(old_price_css).get()
            sale_price = response.xpath(sale_price_css).get()
            sale_price2 = response.xpath(sale_price_css2).get()

            yield {
                'id': product['id'],
                'title': title.strip() if title else product['title'],
                'old_price': old_price.strip() if old_price else product['old_price'],
                'sale_price': sale_price.strip() if sale_price else sale_price2.strip() if sale_price2 else product['sale_price'],
                'link': response.urljoin(product['link']),
                'extraction_date': extraction_date
            }
