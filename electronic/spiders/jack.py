import scrapy
from datetime import datetime


class SpotahomeSpider(scrapy.Spider):
    name = "jack"
    allowed_domains = ["jackvapestore.com"]
    
    start_urls = ["https://jackvapestore.com/2-inicio"] + \
                 [f"https://jackvapestore.com/2-inicio?page={page}" for page in range(1, 32)]  # 1 through 31

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        listings = response.xpath("//*[@id='js-product-list']/div[1]/article") 
        
        for index, listing in enumerate(listings,start=1):
            title = listing.xpath("./div/div[2]/h3/a/text()").get()
            price = listing.xpath("./div/div[2]/div/span[2]/span[1]/text()").get()
            link = listing.xpath("./div/a/@href").get()
            
            yield {
                'id': index,
                'title': title,
                'price': price,
                'link': response.urljoin(link),
                'exdate': extraction_date
                
            }
