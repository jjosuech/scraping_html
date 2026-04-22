import scrapy
from datetime import datetime


class SpotahomeSpider(scrapy.Spider):
    name = "limavaper"
    allowed_domains = ["limavaper.com"]
    
    start_urls = ["https://limavaper.com/todos"] + \
                [f"https://limavaper.com/todos/{page}" for page in range(1, 209)]

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        listings = response.xpath("//div[contains(@class, 'col-md-2 col-sm-3 col-xs-6')]")

        for index, listing in enumerate(listings, start=1):
            title_xpath = ".//div[contains(@class, 'product-col')]/h4/text()"
            title = listing.xpath(title_xpath).get()

            old_price_css = ".//div[contains(@class, 'product-col')]/div[contains(@class, 'caption')]/div[1]/div[contains(@class, 'price-old')]/text()"
            sale_price_css = ".//div[contains(@class, 'product-col')]/div[contains(@class, 'caption')]/div[1]/div[contains(@class, 'price-new')]/text()[normalize-space()]"
            # sale_price_css2 = ".//div[contains(@class, 'product-meta')]/div[contains(@class, 'content_price')]/span[1]/text()"
            old_price = listing.xpath(old_price_css).get()
            sale_price = listing.xpath(sale_price_css).get()
            # sale_price2 = listing.xpath(sale_price_css2).get()

            link_xpath = ".//div[contains(@class, 'product-col')]/a/@href"
            link = listing.xpath(link_xpath).get()

            yield {
                'id': index,
                'title': title.strip() if title else '',
                'old_price': old_price.strip() if old_price else '',
                'sale_price': sale_price.strip() if sale_price else '' , #sale_price2.strip()
                'link': response.urljoin(link) if link else '',
                'extraction_date': extraction_date
            }