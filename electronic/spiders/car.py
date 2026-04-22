import scrapy
from datetime import datetime


class SpotahomeSpider(scrapy.Spider):
    name = "autocosmos"
    allowed_domains = ["autocosmos.com.pe"]
    
    start_urls = ["https://autocosmos.com.pe/auto/usado"] + \
                 [f"https://autocosmos.com.pe/auto/usado?pidx={page}" for page in range(1, 5)]

    def parse(self, response):
        extraction_date = datetime.now().strftime('%Y-%m-%d')
        listings = response.xpath("//*[@id='listing-container']/article") 
        
        for index, listing in enumerate(listings,start=1):
            title = listing.xpath("./div/div[2]/h3/a/text()").get()
            price = listing.xpath("./div/div[2]/div/span[2]/span[1]/text()").get()
            link_xpath = ".//a/@href"
            link = listing.xpath(link_xpath).get()
            
            yield {
                'id': index,
                'title': title,
                'price': price,
                'link': response.urljoin(link) if link else '',
                'exdate': extraction_date
            }
