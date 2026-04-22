import scrapy
from datetime import datetime


class SpotahomeSpider(scrapy.Spider):
    name = "vapor"
    allowed_domains = ["vaporclub.pe/"]
    
    start_urls = [ "https://www.vaporclub.pe/collections/all" ]+ \
                [ f"https://www.vaporclub.pe/collections/all?page={page}" for page in range(1, 21)]
    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        listings = response.xpath("//div[contains(@class,'product-list--collection')]/div[contains(@class, 'product-item')]")

        for index, listing in enumerate(listings, start=1):
            marca = listing.xpath(".//div[contains(@class, 'product-item__info')]/div[contains(@class, 'product-item__info-inner')]/a[1]/text()").get()
            title = listing.xpath(".//div[contains(@class, 'product-item__info')]/div[contains(@class, 'product-item__info-inner')]/a[2]/text()").get()
            link = listing.xpath(".//a/@href").get()
            regular_price_1 = listing.xpath(".//div[contains(@class, 'product-item__info')]/div[contains(@class, 'product-item__info-inner')]/div[1]/span[contains(@class, 'price--highlight')]/text()").get()
            price = listing.xpath(".//div[contains(@class, 'product-item__info')]/div[contains(@class, 'product-item__info-inner')]/div[1]/span[1]/text()").get()
            price2 = listing.xpath(".//div[contains(@class, 'product-item__info')]/div[contains(@class, 'product-item__info-inner')]/div[1]/span[contains(@class, 'price--compare')]/text()").get()
            price = price.strip() if price else ''
            price2 = price2.strip() if price2 else ''
            # sale_price = listing.xpath(".//div[2]/div/div/span[1]/text()").get()
            yield {
                'id': index,
                'marca': marca,
                'title': title,
                # 'price_info': price_info,
                'sale price': regular_price_1 if regular_price_1 else '',
                'regular': price2 if price2 else price if price else '',
                # 'sale_price': sale_price,
                'link': response.urljoin(link),
                'exdate': extraction_date
            }
