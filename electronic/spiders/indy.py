import scrapy
from datetime import datetime


class SpotahomeSpider(scrapy.Spider):
    name = "indy"
    allowed_domains = ["www.indyperuvapes.pe"]
    
    start_urls = ["https://www.indyperuvapes.pe/collections/star-x",
                  "https://www.indyperuvapes.pe/collections/mtrx-25000",
                  "https://www.indyperuvapes.pe/collections/geek-bar-pulse",
                  "https://www.indyperuvapes.pe/collections/lost-mary",
                  "https://www.indyperuvapes.pe/collections/elfbar",
                  "https://www.indyperuvapes.pe/collections/meloso",
                  "https://www.indyperuvapes.pe/collections/life-pod-eco-kit",
                  "https://www.indyperuvapes.pe/collections/dragbar",
                  "https://www.indyperuvapes.pe/collections/escobars",
                  "https://www.indyperuvapes.pe/collections/hqd-cuvie-bar-7000-puffs",
                  "https://www.indyperuvapes.pe/collections/tyson",
                  "https://www.indyperuvapes.pe/collections/skwezed",
                  "https://www.indyperuvapes.pe/collections/yummi",
                  "https://www.indyperuvapes.pe/collections/lost-vape-orion-bar-7500-puffs",
                  "https://www.indyperuvapes.pe/collections/resistencias",
                  "https://www.indyperuvapes.pe/collections/sistema-pod",
                  "https://www.indyperuvapes.pe/collections/kit-de-inicio",
                  "https://www.indyperuvapes.pe/collections/kit-intermedio",
                  "https://www.indyperuvapes.pe/collections/kit-avanzado",
                  "https://www.indyperuvapes.pe/collections/sales",
                  "https://www.indyperuvapes.pe/collections/blvk",
                  "https://www.indyperuvapes.pe/collections/equipos-cali",
                  "https://www.indyperuvapes.pe/collections/papeles-cali",
                  "https://www.indyperuvapes.pe/collections/pipas-cali",
                  "https://www.indyperuvapes.pe/collections/accesorios-cali",
                  "https://www.indyperuvapes.pe/collections/juul",
                ]

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        listings = response.xpath("//div[contains(@class, 'productarray')]/div")

        for index, listing in enumerate(listings, start=1):
            title_xpath = ".//div[contains(@class, 'product-meta')]/div[contains(@class, 'grid-view-item__title')]/a/text()"
            title = listing.xpath(title_xpath).get()

            old_price_css = ".//div[contains(@class, 'product-meta')]/div[contains(@class, 'content_price')]/span[contains(@class, 'old-price')]/text()"
            sale_price_css = ".//div[contains(@class, 'product-meta')]/div[contains(@class, 'content_price')]/span[contains(@class, 'sale-price')]/text()"
            sale_price_css2 = ".//div[contains(@class, 'product-meta')]/div[contains(@class, 'content_price')]/span[1]/text()"
            old_price = listing.xpath(old_price_css).get()
            sale_price = listing.xpath(sale_price_css).get()
            sale_price2 = listing.xpath(sale_price_css2).get()

            link_xpath = ".//div[contains(@class, 'product-image-container')]/a/@href"
            link = listing.xpath(link_xpath).get()

            yield {
                'id': index,
                'title': title.strip() if title else '',
                'old_price': old_price.strip() if old_price else '',
                'sale_price': sale_price.strip() if sale_price else sale_price2.strip(),
                'link': response.urljoin(link) if link else '',
                'extraction_date': extraction_date
            }