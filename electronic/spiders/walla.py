import scrapy
from datetime import datetime
#mira, si, sm, jm, ch, ba, sur, molina, lince, magdalena

class WallaSpider(scrapy.Spider):
    name = "walla"
    allowed_domains = ["es.wallapop.com"]
    start_urls = [
                "https://es.wallapop.com/app/buscar?filters_source=search_box&keywords=coches%20madrid&category_ids=100&longitud=-3.69196&latitud=40.41956"
                  ]

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        # Select all the product items
        product_items = response.css('div[data-qa="product-item"]')
        for index, product in enumerate(product_items, start=1):  # Limiting to first 5 entries
            # Extracting the product name and price
            name_product = product.css('h3[data-testid="typography"]::text').get()
            current_price_raw = product.css('span[data-testid="typography"]::text').get()

            # Processing the price to get only the numerical part
            if current_price_raw:
                current_price_clean = current_price_raw.replace('S/', '').replace(u'\xa0', '').strip()
                current_price = ''.join(filter(lambda x: x.isdigit() or x == '.', current_price_clean))
            else:
                current_price = 'No Price'

            # Extracting the store name
            store_name = product.xpath("./preceding::div[contains(@class, 'css-98urqk')][1]//h2/text()").get()

            # Extracting the discount
            discount_raw = product.css('span[data-qa="product-discount"]::text').get()
            discount = discount_raw.strip() if discount_raw else 'No Discount'

            yield {
                'id': index,
                'store_name': store_name.strip() if store_name else 'No Store',
                'name_product': name_product.strip() if name_product else 'No Name',
                'current_price': current_price,
                'discount': discount,
                'exdate': extraction_date
            }
        