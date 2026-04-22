import scrapy
from datetime import datetime

class SpotahomeSpider(scrapy.Spider):
    name = "vapestation"
    allowed_domains = ["vapestation.pe"]
    start_urls = ["https://vapestation.pe/c/desechables/"] + \
                 [f"https://vapestation.pe/c/desechables/page/{page}/" for page in range(1, 21)]

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        listings = response.xpath("//div[contains(@class,'products')]/div")

        for index, listing in enumerate(listings, start=1):
            image_url = listing.xpath(".//a[contains(@class, 'product-image-link')]/img/@src").get()

            yield {
                'id': index,
                'marca': image_url,  # También puedes cambiar este campo si necesitas un nombre específico
                'exdate': extraction_date,
                'image_urls': [image_url],  # Scrapy usará esta URL para descargar la imagen
            }
