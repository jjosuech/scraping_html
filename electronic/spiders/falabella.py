import scrapy
from datetime import datetime

class FalabellaSpider(scrapy.Spider):
    name = "falabella"
    allowed_domains = ["falabella.com.pe"]

    start_urls = [
        "https://www.falabella.com.pe/falabella-pe/category/CATG14817/Cigarros-electronicos",
        "https://www.falabella.com.pe/falabella-pe/search?Ntt=vapes",
        "https://www.falabella.com.pe/falabella-pe/category/CATG14817/Cigarros-electronicos?f.product.brandName=vape",

        #filtrado
        "https://www.falabella.com.pe/falabella-pe/category/CATG14817/Cigarros-electronicos?f.product.brandName=vape+station",
        "https://www.falabella.com.pe/falabella-pe/category/CATG14817/Cigarros-electronicos?facetSelected=true&f.product.brandName=vaporesso",
        "https://www.falabella.com.pe/falabella-pe/category/CATG14817/Cigarros-electronicos?facetSelected=true&totalProducts=229&f.product.brandName=voopoo",

        #por busqueda
        "https://www.falabella.com.pe/falabella-pe/shop/vaporizador-para-fumar",
        "https://www.falabella.com.pe/falabella-pe/search?Ntt=liquido+para+vapear"

    ]

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')

        products = response.css('div[data-testid="ssr-pod"]')

        for index, product in enumerate(products, start=1):

            brand = product.css('b.pod-title::text').get()
            name_product = product.css('b.pod-subTitle::text').get()
            seller = product.css('b.pod-sellerText::text').get()


            # CURRENT PRICE (2 casos)
            current_price_raw = product.css('li[data-internet-price] span::text').get()

            if not current_price_raw:
                current_price_raw = product.css('li[data-event-price] span::text').get()

            if current_price_raw:
                current_price = current_price_raw.replace('S/', '').replace('\xa0', '').strip()
            else:
                current_price = None


            # OLD PRICE
            old_price_raw = product.css('li[data-normal-price] span::text').get()

            if old_price_raw:
                old_price = old_price_raw.replace('S/', '').replace('\xa0', '').strip()
            else:
                old_price = None

            # -------------------------
            # DISCOUNT
            # -------------------------
            discount_raw = product.css('.discount-badge span::text').get()
            discount = discount_raw.strip() if discount_raw else 'No Discount'

            # -------------------------
            # CLEAN DATA
            # -------------------------
            if seller:
                seller = seller.replace('Por ', '').strip()

            if brand:
                brand = brand.strip()

            if name_product:
                name_product = name_product.strip()

            yield {
                'id': index,
                'brand': brand,
                'name_product': name_product,
                'current_price': current_price,
                'discount': discount,
                'old_price': old_price,
                'store_name': seller,
                'source': 'falabella',
                'exdate': extraction_date
            }