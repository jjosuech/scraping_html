import scrapy
import json
import re
from bs4 import BeautifulSoup
from html import unescape
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

        # EXTRAER JSON DEL NEXT DATA
        json_data = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()'
        ).get()

        if not json_data:
            self.logger.warning("No se encontró __NEXT_DATA__")
            return

        # CONVERTIR STRING JSON -> DICCIONARIO
        data = json.loads(json_data)

        # OBTENER PRODUCTOS
        products = data['props']['pageProps']['results']

        for index, product in enumerate(products, start=1):

            # URL
            product_url = product.get('url')

            # MARCA
            brand = product.get('brand')

            # NOMBRE
            name_product = product.get('displayName')

            # SELLER
            seller = product.get('sellerName')

            # PRECIOS
            current_price = None
            old_price = None
            discount = 'No Discount'

            prices = product.get('prices', [])

            for price in prices:

                if price.get('type') in ['internetPrice', 'eventPrice']:

                    current_price = ''.join(price.get('price', []))

                if price.get('type') == 'normalPrice':

                    old_price = ''.join(price.get('price', []))

            # DESCUENTO
            discount_badge = product.get('discountBadge')

            if discount_badge:

                discount = discount_badge.get('label')

            item = {
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

            #DEBUG
            #print("=" * 50)
            #print("PRODUCTO:", name_product)
            #print("URL:", product_url)
            #print("=" * 50)

            # ENTRAR AL DETALLE
            if product_url:

                yield scrapy.Request(
                    url=product_url,
                    callback=self.parse_detail,
                    meta={'item': item},
                    dont_filter=True
                )

            else:

                item['description'] = None
                yield item

    def parse_detail(self, response):

        item = response.meta['item']

        # JSON DEL DETALLE
        json_data = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()'
        ).get()

        if not json_data:

            item['description'] = None
            yield item
            return

        data = json.loads(json_data)

        #DEBUG
        #print("=" * 50)
        #print("DETALLE URL:", response.url)
        #print("=" * 50)

        description = None

        try:

            # BUSCAR DESCRIPCIÓN
            product_data = data['props']['pageProps']

            # DEBUG
            #print(product_data.keys())

            # MUCHAS VECES VIENE ACÁ
            specifications = product_data.get('productData', {})

            description = specifications.get('description')

        except Exception as e:

            print("ERROR:", e)
            

        if description:

            # convertir entidades html
            description = unescape(description)

            # limpiar html
            soup = BeautifulSoup(description, "html.parser")
            description = soup.get_text(separator=" ", strip=True)

            # limpiar espacios extras
            description = re.sub(r'\s+', ' ', description)

        item['description'] = description

        #DEBUG
        #print("DESCRIPCION:")
        #print(description)
        
        yield item