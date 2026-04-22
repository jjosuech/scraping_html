import scrapy
from datetime import datetime
#mira, si, sm, jm, ch, ba, sur, molina, lince, magdalena

class RappiSpider(scrapy.Spider):
    name = "rappi"
    allowed_domains = ["www.rappi.com.pe"]
    start_urls = [
                    # "https://www.rappi.com.pe/search?query=chilcano",
                    # "https://www.rappi.com.pe/search?query=bebidas%20chilcano",
                    # "https://www.rappi.com.pe/search?query=bebidas%20chilcano",
                    # "https://www.rappi.com.pe/search?query=piscano"

                "https://www.rappi.com.pe/search?query=vape",
                "https://www.rappi.com.pe/search?query=cigarro%20electronico",
                "https://www.rappi.com.pe/search?query=desechable",
                "https://www.rappi.com.pe/search?query=descartable",


                "https://www.rappi.com.pe/search?query=geekbar%20vape",
                "https://www.rappi.com.pe/search?query=geekbar%20puff",
                "https://www.rappi.com.pe/search?query=geekbar%20puff%20vape",
                "https://www.rappi.com.pe/search?query=geekbar%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=geekbar%20puff%20vape%20descartable",


                "https://www.rappi.com.pe/search?query=hqd%20vape",
                "https://www.rappi.com.pe/search?query=hqd%20puff",
                "https://www.rappi.com.pe/search?query=hqd%20puff%20vape",
                "https://www.rappi.com.pe/search?query=hqd%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=hqd%20puff%20vape%20descartable",


                "https://www.rappi.com.pe/search?query=dragbar%20vape",
                "https://www.rappi.com.pe/search?query=dragbar%20puff",
                "https://www.rappi.com.pe/search?query=dragbar%20puff%20vape",
                "https://www.rappi.com.pe/search?query=dragbar%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=dragbar%20puff%20vape%20descartable",


                "https://www.rappi.com.pe/search?query=vozol%20vape",
                "https://www.rappi.com.pe/search?query=vozol%20puff",
                "https://www.rappi.com.pe/search?query=vozol%20puff%20vape",
                "https://www.rappi.com.pe/search?query=vozol%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=vozol%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=icewave%20vape",
                "https://www.rappi.com.pe/search?query=icewave%20puff",
                "https://www.rappi.com.pe/search?query=icewave%20puff%20vape",
                "https://www.rappi.com.pe/search?query=icewave%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=icewave%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=nasty%20vape",
                "https://www.rappi.com.pe/search?query=nasty%20puff",
                "https://www.rappi.com.pe/search?query=nasty%20puff%20vape",
                "https://www.rappi.com.pe/search?query=nasty%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=nasty%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=spaceman%20vape",
                "https://www.rappi.com.pe/search?query=spaceman%20puff",
                "https://www.rappi.com.pe/search?query=spaceman%20puff%20vape",
                "https://www.rappi.com.pe/search?query=spaceman%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=spaceman%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=vozol%20vape",
                "https://www.rappi.com.pe/search?query=vozol%20puff",
                "https://www.rappi.com.pe/search?query=vozol%20puff%20vape",
                "https://www.rappi.com.pe/search?query=vozol%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=vozol%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=elfbar%20vape",
                "https://www.rappi.com.pe/search?query=elfbar%20puff",
                "https://www.rappi.com.pe/search?query=elfbar%20puff%20vape",
                "https://www.rappi.com.pe/search?query=elfbar%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=elfbar%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=lost%20mary%20vape",
                "https://www.rappi.com.pe/search?query=lost%20mary%20puff",
                "https://www.rappi.com.pe/search?query=lost%20mary%20puff%20vape",
                "https://www.rappi.com.pe/search?query=lost%20mary%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=lost%20mary%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=b12000%20vape",
                "https://www.rappi.com.pe/search?query=b12000%20puff",
                "https://www.rappi.com.pe/search?query=b12000%20puff%20vape",
                "https://www.rappi.com.pe/search?query=b12000%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=b12000%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=d3000%20vape",
                "https://www.rappi.com.pe/search?query=d3000%20puff",
                "https://www.rappi.com.pe/search?query=d3000%20puff%20vape",
                "https://www.rappi.com.pe/search?query=d3000%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=d3000%20puff%20vape%20descartable",

                "https://www.rappi.com.pe/search?query=b3500%20vape",
                "https://www.rappi.com.pe/search?query=b3500%20puff",
                "https://www.rappi.com.pe/search?query=b3500%20puff%20vape",
                "https://www.rappi.com.pe/search?query=b3500%20puff%20vape%20desechable",
                "https://www.rappi.com.pe/search?query=b3500%20puff%20vape%20descartable",
                
                "https://www.rappi.com.pe/search?query=liquidos%20vape",
                "https://www.rappi.com.pe/search?query=equipos%20fumar"
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

            #A pedido de David agregado precio antiguo
            old_price_raw = product.css('span[data-qa="product-real-price"]::text').get()

            if old_price_raw:
                old_price_clean = old_price_raw.replace('S/', '').replace(u'\xa0', '').strip()
                old_price = ''.join(filter(lambda x: x.isdigit() or x == '.', old_price_clean))
            else:
                old_price = None

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
                'old_price': old_price,
                'discount': discount,
                'exdate': extraction_date
            }
